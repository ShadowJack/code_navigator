from langchain.vectorstores import DeepLake
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA, QAWithSourcesChain
from code_navigator.core.prompts import DOCUMENT_PROMPT, QUESTION_PROMPT, COMBINE_PROMPT
import os

class Chat:
    def __init__(self, deeplake_ds = None):
        """
        Initialize the Chat instance.

        Args:
            deeplake_ds (str, optional): The DeepLake dataset path.
                It can be provided as an argument, or retrieved from the 'DEEPLAKE_DATASET'
                environment variable, or defaults to "./deeplake".

        Returns:
            None
        """
        deeplake_ds = deeplake_ds or os.environ.get("DEEPLAKE_DATASET") or "./deeplake"
        # 1. Connect to vector storage
        db = DeepLake(dataset_path=deeplake_ds, read_only=True, embedding_function=OpenAIEmbeddings())

        # 2. Set up a retriever that'll vectorize user query and run a search on the vector storage
        retriever = db.as_retriever()
        retriever.search_kwargs['distance_metric'] = 'cos' # use cosine to measure distance between vectors (ignores the length of vectors, takes into account only their colliniarity)
        retriever.search_kwargs['fetch_k'] = 10 # Number of documents to pass in a batch to Min-Min-Roughness clustering algorithm
        retriever.search_kwargs['maximal_marginal_relevance'] = True # Optimize for similarity to query AND diversity among the selected documents
        retriever.search_kwargs['k'] = 10 # number of documents to return
        self._retriever = retriever

        # 3. Setup a chat
        llm = ChatOpenAI(model='gpt-3.5-turbo-16k-0613', temperature=0.3)
        #  self._ask = RetrievalQA.from_chain_type(llm, chain_type="stuff", retriever=retriever, return_source_documents=True)
        self._ask = QAWithSourcesChain.from_llm(
                llm,
                document_prompt=DOCUMENT_PROMPT,
                question_prompt=QUESTION_PROMPT,
                combine_prompt=COMBINE_PROMPT,
                )

    def ask(self, question: str) -> str:
        docs = self._retriever.get_relevant_documents(question)
        result = self._ask({'question': question, 'docs': docs})
        print(result)
        return result['answer']
