"""Module for the Flask app object."""
from flask import Flask

app = Flask("Wingredient")


@app.route('/')
def hello_world():
    return 'Hello World!'
