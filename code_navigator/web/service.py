from flask import Flask
from code_navigator.core.data_loader import DataLoader

# Create an instance of the Flask class
app = Flask(__name__)

@app.route("/load")
def load():
    # TODO: get parameters and use them to load correct data
    #  dl = DataLoader()
    #  dl.load()
    return "OK"

