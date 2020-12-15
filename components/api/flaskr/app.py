from flask import Flask, jsonify
from flask_restful import Resource, Api

from flaskr.passwordChecker.dictionary import DictionaryChecker
from flaskr.passwordChecker.robustness import compute_robustness
from flaskr.passwordChecker.substitute import CharacterProjector, ScramblingParams

app = Flask(__name__)
api = Api(app)

character_projector = CharacterProjector(scrambling_params=ScramblingParams(max_trailing=4))
dico_checker = DictionaryChecker(character_projector=character_projector)

dico_checker.load_all_dictionaries('flaskr/resources/dictionaries/long')
print(f'Dictionaries {dico_checker}')


class PasswordChecker(Resource):
    def get(self, password):
        robustness = compute_robustness(password, dico_checker)
        return robustness.serialize()


api.add_resource(PasswordChecker, '/api/<string:password>')
