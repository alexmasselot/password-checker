from unittest import TestCase

from passwordChecker.dictionary import DictionaryChecker
from passwordChecker.substitute import CharacterProjector, ScramblingParams


class DictionaryTest(TestCase):
    def test_load_dictionary(self):
        dico_checker = DictionaryChecker(CharacterProjector())
        dico = dico_checker.load_dictionary('app/resources/test/dictionaries/one.txt')

        self.assertTrue('paf' in dico.words)
        self.assertTrue('ie' in dico.words)

    def test_load_all_dictionaries(self):
        dico_checker = DictionaryChecker(CharacterProjector())
        dico_checker.load_all_dictionaries('app/resources/test/dictionaries')

        got = dico_checker.dictionaries

        self.assertEqual(2, len(got))

        got_one = next((x for x in got if 'one' in x.name), None)
        got_two = next((x for x in got if 'two' in x.name), None)

        self.assertIsNotNone(got_one)
        self.assertIsNotNone(got_two)

        self.assertTrue('chien' in got_one.words)
        self.assertTrue('fiap' in got_two.words)

    def test_load_all_dictionaries_with_trailing(self):
        dico_checker = DictionaryChecker(CharacterProjector(scrambling_params=ScramblingParams(max_trailing=4)))
        dico_checker.load_all_dictionaries('app/resources/test/dictionaries')

        self.assertTrue(dico_checker.contains('chien'))
        self.assertTrue(dico_checker.contains('flap'))
        self.assertFalse(dico_checker.contains('frout'))
        self.assertTrue(dico_checker.contains('flap42'))
        self.assertTrue(dico_checker.contains('flap42!'))
        self.assertFalse(dico_checker.contains('flap42!4545'))
