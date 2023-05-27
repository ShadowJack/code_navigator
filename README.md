# Code navigator bot
A chat-bot that answers questions about a code base.

## Requirements
* Python3.8 or newer
* An account on deeplake.ai
* Access to OpenAI API

## How to run
### As a console app
1. Install required packages with `pip install -r requirements.txt`
2. Rename `.env.template` to `.env` and put your settings there
3. Load your source code with `python run_data_loader.py path_to_source_code [additional_source_code_dirs...]`. 
4. Run chat.py with `python run_chat.py`
5. Start asking questions about the code
### As a web service
There are two options: run in docker or without it.
#### Run in Docker
1. Rename `.env.template` to `.env` and put your settings there
2. Build a Docker image: `docker build -t code_navigator:latest .`
3. Run a container: `docker run -p 8000:8000 code_navigator:latest`
#### Run on the host machine
1. Install required packages with `pip install -r requirements.txt`
2. Rename `.env.template` to `.env` and put your settings there
3. Run the server: `uvicorn web_service:app --reload `

## Web service API
Interactive documentation is available at http://127.0.0.1:8000/docs when running the service locally.

### POST /loadFromGitHub
Process your source code that's located on GitHub and upload it to a vector storage. 
Note: only public repositories are supported for now. To upload you private repo you need to download it to your local machine and then use the [console app](#as-a-console-app) to upload it.

#### Body parameters:
* repositoryUrl - required a path to the repo on GitHub, ex. 'microsoft/slow-cheetah'
* subPaths - optional list of subfolders to load from the repo. If not specified, then the whole repo is processed.
* deeplakeDS - a path to your DeepLake dataset where the processed repo will be uploaded

#### Response:
A json object with a single field: `dataset` containing a path to your DeepLake dataset 

Example:
```
curl -X POST -H 'Content-Type: application/json' -d '{"repositoryUrl": "microsoft/slow-cheetah", "subPaths": ["src/"], "deeplakeDS": "hub://shadowjack/code_navigator_slow_cheetah"}' 'http://127.0.0.1:5000/loadFromGitHub'
```

### POST /sendChatMessage
Start or continue your chat.

#### Body parameters
* message - your chat message
* deeplakeDS - a path to your DeepLake dataset where your processed repo is stored

#### Response
A json object with a single field: `response`. It's a response to your chat message

Example:
```
curl -X POST -H 'Content-Type: application/json' -d '{"message": "Please describe responsibilities of TransformationTaskLogger", "deeplakeDS": "hub://shadowjack/code_navigator_slow_cheetah"}' 'http://127.0.0.1:5000/sendChatMessage'
```
