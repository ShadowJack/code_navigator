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
TBD
