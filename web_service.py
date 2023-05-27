from flask import Flask, request, jsonify
from pydantic import BaseModel, ValidationError
from .code_navigator.core.data_loader import GitHubDataLoader
from .code_navigator.core.chat import Chat
from typing import List, Dict

# Create an instance of the Flask class
app = Flask(__name__)
chats: Dict[str, Chat] = {}

class LoadRequest(BaseModel):
    repositoryUrl: str
    subPaths: List[str] = []
    deeplakeDS: str

@app.route("/loadFromGitHub", methods=['POST'])
def load():
    try:
        data = request.get_json()
        payload = LoadRequest(**data)
        dl = GitHubDataLoader(deeplake_ds=payload.deeplakeDS)
        ds = dl.load(payload.repositoryUrl, sub_paths=payload.subPaths)
        return jsonify({'dataset': ds.dataset_path}), 200
    except ValidationError as e:
        return jsonify({'errors': e.errors()}), 400

class ChatMessageRequest(BaseModel):
    message: str
    deeplakeDS: str

@app.route("/sendChatMessage", methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        payload = ChatMessageRequest(**data)
        ds = payload.deeplakeDS
        if ds not in chats:
            chats[ds] = Chat(ds)

        chat = chats[ds]
        response = chat.ask(payload.message)

        return jsonify({'response': response}), 200
    except ValidationError as e:
        return jsonify({'errors': e.errors()}), 400
