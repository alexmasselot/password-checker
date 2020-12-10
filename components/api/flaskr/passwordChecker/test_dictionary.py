from unittest import TestCase

from flaskr.passwordChecker.dictionary import load_dictionary, all_dictionaries, load_all_dictionaries


class DictionaryTest(TestCase):
    def test_load_dictionary(self):
        dico = load_dictionary('../resources/test/dictionaries/one.txt')

        self.assertEqual({'paf', 'le', 'chien'}, dico.words)

    def test_load_all_dictionaries(self):
        load_all_dictionaries('../resources/test/dictionaries')

        got = all_dictionaries()

        self.assertEqual(2, len(got))

        got_one = next((x for x in got if 'one' in x.name), None)
        got_two = next((x for x in got if 'two' in x.name), None)

        self.assertIsNotNone(got_one)
        self.assertIsNotNone(got_two)
        self.assertEqual({'paf', 'le', 'chien'}, got_one.words)
        self.assertEqual({'flap', 'la', 'girafe'}, got_two.words)
