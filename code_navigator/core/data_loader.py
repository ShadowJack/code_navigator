from zipfile import ZipFile
import os
import requests
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import DeepLake

# Helper functions
def _split_and_upload(docs, deeplake_ds) -> DeepLake:
    """
    Split documents into chunks and upload them to the vector store
    """
    # Chunk them
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(docs)
    print(len(texts))

    # Save them to vector store
    return DeepLake.from_documents(texts, embedding=OpenAIEmbeddings(client=None,disallowed_special=()), dataset_path=deeplake_ds)

class DataLoader:
    """
    Loader that retrieves source code from the file system
    """
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

    def load(self, *repos) -> DeepLake:
        """
        Load documents from the specified repositories, split them into chunks, and save them to a vector store.

        Args:
            *repos (str): Variable-length argument list of repository directories to load documents from.

        Returns:
            DeepLake dataset

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

        return _split_and_upload(docs, self._deeplake_ds)

class GitHubDataLoader:
    """
    Loader that retrieves source code from GitHub
    """
    def __init__(self,
                 ignored_dirs = [".DStore", "obj", "bin", ".vs", ".idea", ".git", ".gitignore"],
                 file_extensions = [".cs", ".js", ".ts", ".css", "html", ".ex", ".exs"],
                 deeplake_ds = None) -> None:
        """
        Initialize the GitHubDataLoader instance.

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

    def load(self, repository_url, sub_paths = []) -> DeepLake:
        """
        Load documents from the specified GitHub repository, split them into chunks, and save them to a vector store.

        Args:
            repository_url (str): relative url of the GitHub repo
            sub_paths = [] (List[str], optional): A list of repository subdirectories to load documents from. If ommitted, then the whole repository is loaded.

        Returns:
            DeepLake dataset

        Example:
            load('shadowjack/code_navigator')
        """
        # Load documents
        docs = []
        repo_dir = self._download_repository(repository_url)
        for dirpath, _, filenames in os.walk(repo_dir):
            if all(ignored_dir not in dirpath for ignored_dir in self._ignored_dirs) and (len(sub_paths) == 0 or any(sub_path in dirpath for sub_path in sub_paths)):
                for filename in filenames:
                    if any(filename.endswith(file_extension) for file_extension in self._file_extensions):
                        loader = TextLoader(os.path.join(dirpath, filename), encoding="utf-8")
                        docs.extend(loader.load_and_split())

        return _split_and_upload(docs, self._deeplake_ds)

    def _download_repository(self, repository_url: str) -> str:
        """
        Downloads a repository from GitHub into a local file system
        """
        # Create a temporary directory to store the downloaded ZIP file
        temp_dir = './tmp'
        os.makedirs(temp_dir, exist_ok=True)

        # Make a request to the GitHub API to download the repository as a ZIP file
        # NOTE: only public repositories are supported for now
        url = f'https://api.github.com/repos/{repository_url}/zipball'
        response = requests.get(url)
        response.raise_for_status()

        # Save the ZIP file to the temporary directory
        repo_dir = repository_url.replace('/', '_')
        zip_file_path = os.path.join(temp_dir, f"{repo_dir}.zip")
        with open(zip_file_path, 'wb') as file:
            file.write(response.content)

        # Extract the contents of the ZIP file to a target directory
        repo_dir = ""
        with ZipFile(zip_file_path, 'r') as zip_file:
            zip_file.extractall(temp_dir)
            repo_dir = zip_file.namelist()[0]

        # Clean up: delete the temporary ZIP file
        os.remove(zip_file_path)

        return os.path.join(temp_dir, repo_dir)


