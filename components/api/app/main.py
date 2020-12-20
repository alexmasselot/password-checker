from flask import Flask, request, jsonify

from passwordChecker.dictionary import DictionaryChecker
from passwordChecker.robustness import compute_robustness
from passwordChecker.substitute import CharacterProjector, ScramblingParams

app = Flask(__name__, static_url_path='')

character_projector = CharacterProjector(scrambling_params=ScramblingParams(max_trailing=4))
dico_checker = DictionaryChecker(character_projector=character_projector)

dico_checker.load_all_dictionaries('resources/dictionaries')
print(f'Dictionaries {dico_checker}')


@app.route('/api/check', methods=['POST'])
def chek_password():
    password = request.get_json()['password']
    robustness = compute_robustness(password, dico_checker)
    return jsonify(robustness.serialize())


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
