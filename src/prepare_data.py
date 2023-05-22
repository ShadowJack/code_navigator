from dotenv import load_dotenv
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import DeepLake
import sys
import os
from logging import error

load_dotenv()
ignored_dirs = [".DStore", "obj", "bin", ".vs", ".idea", ".git", ".gitignore"]
file_extensions = [".cs", ".js", ".ts", ".css", "html", ".ex", ".exs"]
deeplake_ds = os.environ.get("DEEPLAKE_DATASET")

def main():
    """
    Read source code files, vectorize them and save to Deep Lake
    """

    if len(sys.argv) < 2:
        error("A path to a code base directory must be provided")

    # 1. Load documents
    repo_dir = sys.argv[1]
    docs = []
    for dirpath, _, filenames in os.walk(repo_dir):
        if all(ignored_dir not in dirpath for ignored_dir in ignored_dirs):
            for filename in filenames:
                if any(filename.endswith(file_extension) for file_extension in file_extensions):
                    loader = TextLoader(os.path.join(dirpath, filename), encoding="utf-8")
                    docs.extend(loader.load_and_split())

    # 2. Chunk them
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(docs)
    print(len(texts))

    # 3. Save them to vector store
    DeepLake.from_documents(texts, embedding=OpenAIEmbeddings(disallowed_special=()), dataset_path=deeplake_ds)

if __name__ == "__main__":
    main()
