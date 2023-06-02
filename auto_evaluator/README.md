# `VectorDB Auto-evaluator` :brain: :memo:

A modified version of the [langchain-ai/auto-evaluator](https://github.com/langchain-ai/auto-evaluator/tree/main/streamlit)

**App**

There are several architectures for retrieval:

![image](https://github.com/langchain-ai/auto-evaluator/assets/122662504/e8763dc0-474d-4c59-97c7-00c70cbc974e)

Here, we connect auto-evaluator to Pinecone in order to test performance of the chain with and without metadata filtering (architecture 3). 

`1) Pinecone without metadata filtering`
* Just query raw vector store without additional metadata filtering

`2) Pinecone w/ self-querying`

* See background on self-querying retriever [here](https://python.langchain.com/en/latest/modules/indexes/retrievers/examples/self_query_retriever.html)
* See example `metadata_field_info` [here](https://github.com/langchain-ai/auto-evaluator/blob/d3e6a7eaff0ac0a04904cdafcefc3980d4321014/streamlit/self_query_retriever_lex.py#L3)
* The `SelfQueryRetriever` will try to extract metadata filters from the question

`3) Kor filtering`

* See background on Kor [here](https://eyurtsev.github.io/kor/tutorial.html)
* See example `schema` for Kor [here](https://github.com/langchain-ai/auto-evaluator/blob/d3e6a7eaff0ac0a04904cdafcefc3980d4321014/streamlit/kor_retriever_lex.py#L8) 
* Define a `kor_retriever` that will try to extract metadata filters from the question
* Here is the the problem that Kor filtering can help solve:

![image](https://github.com/langchain-ai/auto-evaluator/assets/122662504/7e12fd3b-4f97-4afa-a3ab-d325f16c4a35)

**Run as Streamlit app**

`pip install -r requirements.txt`

`streamlit run auto-evaluator.py`

**Inputs**
 
`retriever_type` - Retrieval method

`num_neighbors` - Neighbors for retrieval 

`embeddings` - Embeddings in your Pinecone vectorDB

`model` - LLM for summarization of retrieved chunks 

`grade_prompt` - Prompt choice for model self-grading

**Blog**

https://rlancemartin.notion.site/Auto-Evaluation-of-Metadata-Filtering-18502448c85240828f33716740f9574b

**Disclaimer**

```You will need an OpenAI API key with access to `GPT-4` for the default grading, but this can be modified in grade_model_retrieval and grade_model_answer if needed [here](https://github.com/langchain-ai/auto-evaluator/blob/d3e6a7eaff0ac0a04904cdafcefc3980d4321014/streamlit/auto-evaluator.py#L135).```
