import os

from flask import Flask, jsonify

from flaskr.passwordChecker.dictionary import load_all_dictionaries, all_dictionaries
from flaskr.passwordChecker.robustness import compute_robustness

app = Flask(__name__)

load_all_dictionaries('flaskr/resources/dictionaries/250')
load_all_dictionaries('flaskr/resources/dictionaries/long', substitute_characters=False)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/<password>')
def analyze(password):
    robustness = compute_robustness(password)
    return jsonify(robustness.serialize())
