from flask import Flask, request, jsonify

from flaskr.passwordChecker.dictionary import DictionaryChecker
from flaskr.passwordChecker.robustness import compute_robustness
from flaskr.passwordChecker.substitute import CharacterProjector, ScramblingParams

app = Flask(__name__)

character_projector = CharacterProjector(scrambling_params=ScramblingParams(max_trailing=4))
dico_checker = DictionaryChecker(character_projector=character_projector)

dico_checker.load_all_dictionaries('flaskr/resources/dictionaries/long')
print(f'Dictionaries {dico_checker}')


@app.route('/api/check', methods=['POST'])
def chek_password():
    password = request.get_json()['password']
    robustness = compute_robustness(password, dico_checker)
    return jsonify(robustness.serialize())
