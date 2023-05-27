from fastapi import FastAPI
from pydantic import BaseModel, ValidationError
from code_navigator.core.data_loader import GitHubDataLoader
from code_navigator.core.chat import Chat
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

# Create an instance of the Flask class
app = FastAPI()
chats: Dict[str, Chat] = {}

class LoadRequest(BaseModel):
    repositoryUrl: str
    subPaths: List[str] = []
    deeplakeDS: str

@app.post("/loadFromGitHub")
def load(payload: LoadRequest):
    dl = GitHubDataLoader(deeplake_ds=payload.deeplakeDS)
    ds = dl.load(payload.repositoryUrl, sub_paths=payload.subPaths)
    return {'dataset': ds.dataset_path}

class ChatMessageRequest(BaseModel):
    message: str
    deeplakeDS: str

@app.post("/sendChatMessage")
def send_message(payload: ChatMessageRequest):
    ds = payload.deeplakeDS
    if ds not in chats:
        chats[ds] = Chat(ds)

    chat = chats[ds]
    response = chat.ask(payload.message)

    return {'response': response}
