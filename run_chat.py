from dotenv import load_dotenv
from code_navigator.core.chat import Chat

load_dotenv()

def main():
    """
    The goal of this bot is to respond to questions about the code base that's loaded with a prepare_data.py script.
    Example:
        > Human: Who uses module ABC?
        > AI: I found three classes where this module is used: Test1, BusinessLogic, SomeController
        > Human: What is the class structure of BCD?
        > AI: BCD -> MegaBCD -> IModel
        > Human: Where is the controller that handles requests related to user registration and authentication?
        > AI: Here is is: API/Controllers/UsersController.cs
    """
    chat = Chat()
    while True:
        question = input("Question: ")
        answer = chat.ask(question)
        print(f"Answer: {answer}")

if __name__ == "__main__":
    main()
