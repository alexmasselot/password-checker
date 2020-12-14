from unittest import TestCase

from flaskr.passwordChecker.dictionary import load_dictionary, DictionaryChecker
from flaskr.passwordChecker.substitute import SubstitutionParams


class DictionaryTest(TestCase):
    def test_load_dictionary(self):
        dico = load_dictionary('flaskr/resources/test/dictionaries/one.txt', SubstitutionParams())

        self.assertTrue('p@F' in dico.words)

    def test_load_all_dictionaries(self):
        dicoChecker = DictionaryChecker()
        dicoChecker.load_all_dictionaries('flaskr/resources/test/dictionaries', SubstitutionParams())

        got = dicoChecker.dictionaries
        print(got)

        self.assertEqual(2, len(got))

        got_one = next((x for x in got if 'one' in x.name), None)
        got_two = next((x for x in got if 'two' in x.name), None)

        self.assertIsNotNone(got_one)
        self.assertIsNotNone(got_two)

        self.assertTrue('chien' in got_one.words)
        self.assertTrue('fi@p' in got_two.words)
