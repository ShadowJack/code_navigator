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
1. Install required packages with `pip install -r requirements.txt`
2. Rename `.env.template` to `.env` and put your settings there
3. Set up additional environment variables: `export FLASK_APP=web_service.py && export FLASK_ENV=development`
4. Run the server: `flask run`

## Web service API

### POST /loadFromGitHub
Process your source code that's located on GitHub and upload it to a vector storage. 
Note: only public repositories are supported for now. To upload you private repo you need to download it to your local machine and then use the [console app](#As a console app) to upload it.

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
