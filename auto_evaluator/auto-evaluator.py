import os
import json
from dotenv import load_dotenv
import time
import deeplake
import pandas as pd
import altair as alt
import streamlit as st
import universal_retriever
from typing import List
from langchain.vectorstores.base import VectorStoreRetriever
from langchain.vectorstores import DeepLake
from langchain.llms import Anthropic
from langchain.chat_models import ChatOpenAI
from langchain.evaluation.qa import QAEvalChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.combine_documents.base import BaseCombineDocumentsChain
from langchain.chains.question_answering import load_qa_chain
from langchain.schema import Document, BaseRetriever
from prompts import GRADE_DOCS_PROMPT, GRADE_ANSWER_PROMPT, GRADE_ANSWER_PROMPT_FAST, GRADE_ANSWER_PROMPT_BIAS_CHECK, GRADE_ANSWER_PROMPT_OPENAI, QA_CHAIN_PROMPT_PROGRAMMING

load_dotenv()

# Keep dataframe in memory to accumulate experimental results
if "existing_df" not in st.session_state:
    summary = pd.DataFrame(columns=['model',
                                    'retriever',
                                    'embedding',
                                    'num_neighbors',
                                    'Latency',
                                    'Retrieval score',
                                    'Answer score'])
    st.session_state.existing_df = summary
else:
    summary = st.session_state.existing_df

@st.cache_resource
def make_llm(model_version: str) -> ChatOpenAI | Anthropic:
    """
    Make LLM from model version
    @param model_version: model_version
    @return: LLM
    """
    if (model_version == "gpt-3.5-turbo") or (model_version == "gpt-4"):
        chosen_model = ChatOpenAI(model_name=model_version, temperature=0)
    elif model_version == "anthropic":
        chosen_model = Anthropic(temperature=0)
    else:
        st.warning("`Model version not recognized. Using gpt-3.5-turbo`", icon="⚠️")
        chosen_model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    return chosen_model

@st.cache_resource
def make_retriever(retriever_type: str, dataset: DeepLake, llm: ChatOpenAI | Anthropic) -> BaseRetriever:
    """
    Make document retriever
    @param retriever_type: retriever type
    @param llm: LLM
    @return: BaseRetriever
    """
    st.info("`Connecting to DeepLake ...`")

    return universal_retriever.make_retriever(retriever_type, dataset, llm, num_neighbors)

def make_chain(llm: ChatOpenAI | Anthropic) -> BaseCombineDocumentsChain:
    """
    Make retrieval chain
    @param llm: LLM
    @return: QA chain
    """

    qa_chain = load_qa_chain(llm, chain_type="stuff", prompt=QA_CHAIN_PROMPT_PROGRAMMING)

    return qa_chain


def grade_model_answer(predicted_dataset: List, predictions: List, grade_answer_prompt: str) -> List:
    """
    Grades the distilled answer based on ground truth and model predictions.
    @param predicted_dataset: A list of dictionaries containing ground truth questions and answers.
    @param predictions: A list of dictionaries containing model predictions for the questions.
    @param grade_answer_prompt: The prompt level for the grading.
    @return: A list of scores for the distilled answers.
    """
    # Grade the distilled answer
    st.info("`Grading model answer ...`")
    # Set the grading prompt based on the grade_answer_prompt parameter
    if grade_answer_prompt == "Fast":
        prompt = GRADE_ANSWER_PROMPT_FAST
    elif grade_answer_prompt == "Descriptive w/ bias check":
        prompt = GRADE_ANSWER_PROMPT_BIAS_CHECK
    elif grade_answer_prompt == "OpenAI grading prompt":
        prompt = GRADE_ANSWER_PROMPT_OPENAI
    else:
        prompt = GRADE_ANSWER_PROMPT

    # Create an evaluation chain
    eval_chain = QAEvalChain.from_llm(
        llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0),
        prompt=prompt
    )

    # Evaluate the predictions and ground truth using the evaluation chain
    graded_outputs = eval_chain.evaluate(
        predicted_dataset,
        predictions,
        question_key="question",
        prediction_key="result"
    )

    return graded_outputs


def grade_docs_retrieval(gt_dataset: List, predictions: List):
    """
    Grades the relevance of retrieved documents based on ground truth and model predictions.
    @param gt_dataset: list of dictionaries containing ground truth questions and answers.
    @param predictions: list of dictionaries containing model predictions for the questions
    @return: list of scores for the retrieved documents.
    """
    # Grade the docs retrieval
    st.info("`Grading relevance of retrieved docs ...`")

    # Set the grading prompt based on the grade_docs_prompt parameter
    prompt = GRADE_DOCS_PROMPT

    # Create an evaluation chain
    eval_chain = QAEvalChain.from_llm(
        llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0),
        prompt=prompt
    )

    # Evaluate the predictions and ground truth using the evaluation chain
    graded_outputs = eval_chain.evaluate(
        gt_dataset,
        predictions,
        question_key="question",
        prediction_key="result"
    )
    return graded_outputs


def run_evaluation(chain, retriever: BaseRetriever, eval_set, grade_prompt):
    """
    Runs evaluation on a model's performance on a given evaluation dataset.
    @param chain: Model chain used for answering questions
    @param retriever:  Document retriever used for retrieving relevant documents
    @param eval_set: List of dictionaries containing questions and corresponding ground truth answers
    @param grade_prompt: String prompt used for grading model's performance
    @return: A tuple of four items:
    - answers_grade: A dictionary containing scores for the model's answers.
    - retrieval_grade: A dictionary containing scores for the model's document retrieval.
    - latencies_list: A list of latencies in seconds for each question answered.
    - predictions_list: A list of dictionaries containing the model's predicted answers and relevant documents for each question.
    """
    st.info("`Running evaluation ...`")
    predictions_list = []
    retrieved_docs = []
    gt_dataset = []
    latencies_list = []

    for data in eval_set:

        # Get answer and log latency
        start_time = time.time()

        # Get docs
        docs = retriever.get_relevant_documents(data["question"])
        print("--DOCS--")
        if not docs:
            docs=[Document(page_content="I was unable to recover any information about the question!")]
        print(docs)

        # Get answer
        answer = chain.run(input_documents=docs,question=data["question"])
        predictions_list.append({"question": data["question"], "answer": data["answer"], "result": answer})
        gt_dataset.append(data)
        end_time = time.time()
        elapsed_time = end_time - start_time
        latencies_list.append(elapsed_time)

        # Get doc text
        retrieved_doc_text = ""
        for i, doc in enumerate(docs):
            retrieved_doc_text += "Doc %s: " % str(i + 1) + doc.page_content + " "
        retrieved = {"question": data["question"], "answer": data["answer"], "result": retrieved_doc_text}
        retrieved_docs.append(retrieved)

    # Grade docs and answer
    answers_grade = grade_model_answer(gt_dataset, predictions_list, grade_prompt)
    retrieval_grade = grade_docs_retrieval(gt_dataset, retrieved_docs)
    return answers_grade, retrieval_grade, latencies_list, predictions_list

# Auth
st.sidebar.image("img/diagnostic.jpg")

with st.sidebar.form("user_input"):

    # DeepLake params
    oai_api_key = st.text_input("`OpenAI API Key:`", type="password").strip()
    deeplake_api_key = st.text_input("`DeepLake API Key:`", type="password").strip()
    deeplake_ds = st.text_input("`DeepLake datasource:`", type="password").strip()

    retriever_type = st.radio("`Choose retriever`",
                              ("DeepLake",
                               "DeepLake w/ self-querying",
                               "Kor filtering"),
                              index=0)

    num_neighbors = st.select_slider("`Choose # chunks to retrieve`",
                                     options=[3, 4, 5, 6, 7, 8])

    embeddings = st.radio("`Choose embeddings`",
                          ("HuggingFace",
                           "OpenAI"),
                          index=1)

    model = st.radio("`Choose model`",
                     ("gpt-3.5-turbo",
                      "gpt-4"),
                     index=0)

    grade_prompt = st.radio("`Grading style prompt`",
                            ("Fast",
                             "Descriptive",
                             "Descriptive w/ bias check",
                             "OpenAI grading prompt"),
                            index=3)

    submitted = st.form_submit_button("Submit evaluation")

# App
st.header("`VectorDB auto-evaluator`")
st.info(
    "`I am an evaluation tool for question-answering using an existing vectorDB (currently DeepLake is supported) and an eval set. "
    "I will generate and grade an answer to each eval set question with the user-specific retrival setting, such as metadata filtering or self-querying retrieval."
    " Experiments with different configurations are logged. For an example eval set, see eval_sets/lex-pod-eval.json.`")

with st.form(key='file_inputs'):

    uploaded_eval_set = st.file_uploader("`Please upload eval set (.json):` ",
                                         type=['json'],
                                         accept_multiple_files=False)

    submitted = st.form_submit_button("Submit files")

# Build an index from the supplied docs
if uploaded_eval_set and deeplake_api_key and deeplake_ds:

    # Set API key
    if not os.environ["OPENAI_API_KEY"]:
        os.environ["OPENAI_API_KEY"] = oai_api_key

    # Set embeddings (must match your DeepLake DB)
    if embeddings == "OpenAI":
        embedding = OpenAIEmbeddings()
    elif embeddings == "HuggingFace":
        embedding = HuggingFaceEmbeddings()

    # Set DeepLake
    dataset = DeepLake(dataset_path=str(deeplake_ds), read_only=True, embedding_function=embedding)

    # Eval set
    eval_set = json.loads(uploaded_eval_set.read())

    # Make LLM
    llm = make_llm(model)

    # Make retriver
    st.info("`Connecting to DeepLake ...`")
    retriever = make_retriever(retriever_type, dataset, llm)

    # Make chain
    qa_chain = make_chain(llm)

    # Grade model
    graded_answers, graded_retrieval, latency, predictions = run_evaluation(qa_chain, retriever, eval_set, grade_prompt,
                                                                        retriever_type)

    # Assemble outputs
    d = pd.DataFrame(predictions)
    d['answer score'] = [g['text'] for g in graded_answers]
    d['docs score'] = [g['text'] for g in graded_retrieval]
    d['latency'] = latency

    # Summary statistics
    mean_latency = d['latency'].mean()
    correct_answer_count = len([text for text in d['answer score'] if "Incorrect" not in text])
    correct_docs_count = len([text for text in d['docs score'] if "Incorrect" not in text])
    percentage_answer = (correct_answer_count / len(graded_answers)) * 100
    percentage_docs = (correct_docs_count / len(graded_retrieval)) * 100

    st.subheader("`Run Results`")
    st.info(
        "`I will grade the chain based on: 1/ the relevance of the retrived documents relative to the question and 2/ "
        "the summarized answer relative to the ground truth answer. You can see (and change) to prompts used for "
        "grading in text_utils`")
    st.dataframe(data=d, use_container_width=True)

    # Accumulate results
    st.subheader("`Aggregate Results`")
    st.info(
        "`Retrieval and answer scores are percentage of retrived documents deemed relevant by the LLM grader ("
        "relative to the question) and percentage of summarized answers deemed relevant (relative to ground truth "
        "answer), respectively. The size of point correponds to the latency (in seconds) of retrieval + answer "
        "summarization (larger circle = slower).`")
    new_row = pd.DataFrame({'model': [model],
                            'retriever': [retriever_type],
                            'embedding': [embeddings],
                            'num_neighbors': [num_neighbors],
                            'Latency': [mean_latency],
                            'Retrieval score': [percentage_docs],
                            'Answer score': [percentage_answer]})
    summary = pd.concat([summary, new_row], ignore_index=True)
    st.dataframe(data=summary, use_container_width=True)
    st.session_state.existing_df = summary

    # Dataframe for visualization
    show = summary.reset_index().copy()
    show.columns = ['expt number', 'model', 'retriever', 'embedding', 'num_neighbors', 'Latency', 'Retrieval score','Answer score']
    show['expt number'] = show['expt number'].apply(lambda x: "Expt #: " + str(x + 1))
    c = alt.Chart(show).mark_circle().encode(x='Retrieval score',
                                                y='Answer score',
                                                size=alt.Size('Latency'),
                                                color='expt number',
                                                tooltip=['expt number', 'Retrieval score', 'Latency', 'Answer score'])
    st.altair_chart(c, use_container_width=True, theme="streamlit")

else:
    st.warning('Please specify a DeepLake index and add an eval set.', icon="⚠️")
