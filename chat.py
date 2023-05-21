from langchain.chat_models import ChatOpenAI
from langchain.schema import (
        AIMessage,
        HumanMessage,
        SystemMessage
    )
from typing import List, Union

def main():
    """
    The goal of this bot is to ask him questions about the code base.
    Example: 
        > Human: Who uses module ABC?
        > AI: I found three classes where this module is used: Test1, BusinessLogic, SomeController
        > Human: Where is the controller that handles requests related to user registration and authentication?
        > AI: API/Controllers/UsersController.cs
    """

    # TODO:
    # 1. Take request from user, vectorize it, finds related documents
    # 2. Give LLM found documents and ask to respond to the question

if __name__ == "__main__":
    main()
