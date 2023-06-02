from typing import List
from langchain.schema import Document, BaseRetriever
from langchain.llms import Anthropic
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import DeepLake
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.schema import AttributeInfo
from kor.extraction import create_extraction_chain
from kor.nodes import Object, Text

## Kor setup

class KorRetriever(BaseRetriever):
    """
    A wrapper around Kor filtering + DeepLake retrieval
    """

    def __init__(self,
                 dataset: DeepLake,
                 llm: ChatOpenAI | Anthropic,
                 num_neighbors: int):
        """Initialize KorRetriever"""
        schema = Object(
            id = "episode_id",
            description = "An ID for each Lex Fridman podcast episode",
            attributes = [
                Text(
                    id="episode_id",
                    description="The podcast ID.",
                )
            ],
            examples = [
                ("What does episode 333 say about AI?", [{"episode_id": "0333"}]),
                ("What does episode #231 say about dogs?", [{"episode_id": "0231"}]),
                ("What is the summary of episode 50?",[{"episode_id": "050"}])
            ],
            many = True,
        )

        self._chain = create_extraction_chain(llm, schema)
        self._dataset = dataset
        self._num_neighbors = num_neighbors

    def get_relevant_documents(self, query: str) -> List[Document]:
        # Metadata extraction
        results = self._chain.predict_and_parse(text=(query.strip()))["data"]['episode_id']
        print("RESULTS in KOR:")
        print(results)

        # Get results
        if results:
            metadata_filter = {'id':results[0]['episode_id']}
            return self._dataset.similarity_search(query=query, k=self._num_neighbors, filter=metadata_filter)

        return []

    async def aget_relevant_documents(self, query: str) -> List[Document]:
        return []

def make_retriever(
             retriever_type: str,
             dataset: DeepLake,
             llm: ChatOpenAI | Anthropic,
             num_neighbors: int) -> BaseRetriever | None:
    """
    Make document retriever based on retriever_type
    @param retriever_type: retriever type
    @param llm: LLM
    """

    # Retriver type
    if retriever_type == "DeepLake":
        retriever = dataset.as_retriever()
        retriever.search_kwargs['distance_metric'] = 'cos'
        retriever.search_kwargs['fetch_k'] = 20
        retriever.search_kwargs['maximal_marginal_relevance'] = True
        retriever.search_kwargs['k'] = num_neighbors
        return retriever
    elif retriever_type == "DeepLake w/ self-querying":
        metadata_field_info=[
            AttributeInfo(
                name="source",
                description="Path to a file with the source code",
                type="string",
            ),
        ]
        document_content_description = "Source code of a software program"
        return SelfQueryRetriever.from_llm(llm, dataset, document_content_description, metadata_field_info, verbose=True, k=num_neighbors)
    elif retriever_type == "Kor filtering":
        return KorRetriever(dataset, llm, num_neighbors)
