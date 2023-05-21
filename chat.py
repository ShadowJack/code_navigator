from langchain.vectorstores import DeepLake
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os

load_dotenv()
deeplake_ds = os.environ.get("DEEPLAKE_DATASET") or "./deeplake"

def main():
    """
    The goal of this bot is to respond to questions about the code base that's loaded with a prepare_data.py script.
    Example:
        > Human: Who uses module ABC?
        > AI: I found three classes where this module is used: Test1, BusinessLogic, SomeController
        > Human: Where is the controller that handles requests related to user registration and authentication?
        > AI: Here is is: API/Controllers/UsersController.cs
    """


    # 1. Connect to vector storage
    db = DeepLake(dataset_path=deeplake_ds, read_only=True, embedding_function=OpenAIEmbeddings())

    # 2. Set up a retriever that'll vectorize user query and run a search on the vector storage
    retriever = db.as_retriever()
    retriever.search_kwargs['distance_metric'] = 'cos' # use cosine to measure distance between vectors (ignores the length of vectors, takes into account only their colliniarity)
    retriever.search_kwargs['fetch_k'] = 20 # Number of documents to pass in a batch to Min-Min-Roughness clustering algorithm
    retriever.search_kwargs['maximal_marginal_relevance'] = True # Optimize for similarity to query AND diversity among the selected documents
    retriever.search_kwargs['k'] = 20 # number of documents to return

    # 3. Setup a chat and run it
    llm = ChatOpenAI(model='gpt-3.5-turbo')
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    qa = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory)
    while True:
        question = input("Question: ")
        result = qa({"question": question})
        answer = result['answer']
        print(f"Answer: {answer}")

if __name__ == "__main__":
    main()
