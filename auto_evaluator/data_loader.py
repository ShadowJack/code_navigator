import os
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, Language
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
import pinecone

# Helper functions
def _split_and_upload(docs, pinecone_index) -> Pinecone:
    """
    Split documents into chunks and upload them to the vector store
    """
    print(f"Number of documents: {len(docs)}")
    # Chunk them
    text_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.JS, chunk_size=1000, chunk_overlap=0
    )
    texts = text_splitter.split_documents(docs)
    print(len(texts))

    # Save them to vector store
    # initialize pinecone
    pinecone.init(
        api_key="c1234dbd-b5df-4f10-ba76-7c34b7996eb8",  # find at app.pinecone.io
        environment="us-east4-gcp"  # next to api key in console
    )

    return Pinecone.from_documents(texts, embedding=OpenAIEmbeddings(client=None,disallowed_special=()), index_name=pinecone_index)

class DataLoader:
    """
    Loader that retrieves source code from the file system
    """
    def __init__(self,
                 ignored_dirs = [".DStore", "obj", "bin", ".vs", ".idea", ".git", ".gitignore", "_build", "deps", "node_modules"],
                 file_extensions = [".cs", ".json", ".js", ".ts", ".css", ".html", ".ex", ".exs", ".md", ".yml", "Dockerfile", ".config", ".sh"],
                 pinecone_index = None) -> None:
        """
        Initialize the DataLoader instance.
        """
        self._ignored_dirs = ignored_dirs
        self._file_extensions = file_extensions
        self._pinecone_index = pinecone_index or os.environ.get("PINECONE_INDEX") or "code-navigator"

    def load(self, *repos) -> Pinecone:
        # Load documents
        docs = []
        for repo_dir in repos:
            for dirpath, _, filenames in os.walk(repo_dir):
                if all(ignored_dir not in dirpath for ignored_dir in self._ignored_dirs):
                    for filename in filenames:
                        if any(filename.endswith(file_extension) for file_extension in self._file_extensions):
                            loader = TextLoader(os.path.join(dirpath, filename), encoding="utf-8")
                            docs.extend(loader.load_and_split())

        return _split_and_upload(docs, self._pinecone_index)

# The upload script
loader = DataLoader(pinecone_index="code-navigator")
loader.load(f"{os.getenv('HOME')}/Documents/work/powersite")
