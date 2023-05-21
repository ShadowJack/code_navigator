# Code navigator bot
A chat-bot that answers questions about a code base.

## Requirements
* Python3.10
* An account on deeplake.ai
* Access to OpenAI API

## How to run
1. Install required packages with `pip install -r requirements.txt`
2. Rename `.env.template` to `.env` and put your settings there
3. Run prepare_data script with `python prepare_data.py PATH_TO_YOUR_REPOSITORY`. If you don't want to process the whole repository, you can run this command a few times passing subfolders you want to process.
4. Run chat.py with `python chat.py`
5. Start asking questions
