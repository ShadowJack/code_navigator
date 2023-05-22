import sys
from logging import error
from code_navigator.core.data_loader import DataLoader
from dotenv import load_dotenv

load_dotenv()

def main():
    """
    Prepare source code so that it's possible to query it in the question answering phase
    """

    if len(sys.argv) < 2:
        error("A path to a code directory must be provided")
    repo_dirs = sys.argv[1:]

    loader = DataLoader()

    loader.load(*repo_dirs)

if __name__ == "__main__":
    main()
