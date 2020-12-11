from flask import Flask, jsonify

from flaskr.passwordChecker.robustness import compute_robustness

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/<password>')
def analyze(password):
    robustness = compute_robustness(password)
    return jsonify(robustness.serialize())
