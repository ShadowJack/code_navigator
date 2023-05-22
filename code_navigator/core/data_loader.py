from dotenv import load_dotenv
import os
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import DeepLake

class DataLoader:
    def __init__(self,
                 ignored_dirs = [".DStore", "obj", "bin", ".vs", ".idea", ".git", ".gitignore"],
                 file_extensions = [".cs", ".js", ".ts", ".css", "html", ".ex", ".exs"],
                 deeplake_ds = None) -> None:
        """
        Initialize the DataLoader instance.

        Args:
            ignored_dirs (List[str], optional): A list of directory names to ignore.
            file_extensions (List[str], optional): A list of file extensions to consider.
            deeplake_ds (str, optional): The DeepLake dataset path.
                It can be provided as an argument, or retrieved from the 'DEEPLAKE_DATASET'
                environment variable, or defaults to "./deeplake".

        Returns:
            None
        """
        self._ignored_dirs = ignored_dirs
        self._file_extensions = file_extensions
        self._deeplake_ds = deeplake_ds or os.environ.get("DEEPLAKE_DATASET") or "./deeplake"

    def load(self, *repos) -> None:
        """
        Load documents from the specified repositories, split them into chunks, and save them to a vector store.

        Args:
            *repos (str): Variable-length argument list of repository directories to load documents from.

        Returns:
            None

        Raises:
            OSError: If there are any issues with accessing the repositories or reading the files.


        Example:
            load("/path/to/repo1", "/path/to/repo2")
        """
        # Load documents
        docs = []
        for repo_dir in repos:
            for dirpath, _, filenames in os.walk(repo_dir):
                if all(ignored_dir not in dirpath for ignored_dir in self._ignored_dirs):
                    for filename in filenames:
                        if any(filename.endswith(file_extension) for file_extension in self._file_extensions):
                            loader = TextLoader(os.path.join(dirpath, filename), encoding="utf-8")
                            docs.extend(loader.load_and_split())

        # Chunk them
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(docs)
        print(len(texts))

        # Save them to vector store
        DeepLake.from_documents(texts, embedding=OpenAIEmbeddings(client=None,disallowed_special=()), dataset_path=self._deeplake_ds)
