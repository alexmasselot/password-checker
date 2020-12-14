from flask import Flask, jsonify

from flaskr.passwordChecker.dictionary import DictionaryChecker
from flaskr.passwordChecker.robustness import compute_robustness
from flaskr.passwordChecker.substitute import SubstitutionParams

app = Flask(__name__)

dicoChecker = DictionaryChecker()
dicoChecker.load_all_dictionaries('flaskr/resources/dictionaries/250',
                                  SubstitutionParams(substitute_characters=2, append_punctuation=True,
                                                     append_number=True))
dicoChecker.load_all_dictionaries('flaskr/resources/dictionaries/long',
                                  SubstitutionParams(substitute_characters=0, append_punctuation=False,
                                                     append_number=False))
print(f'Dictionaries {dicoChecker}')


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/<password>')
def analyze(password):
    robustness = compute_robustness(password, dicoChecker)
    return jsonify(robustness.serialize())



