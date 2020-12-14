from itertools import chain

from flaskr.passwordChecker.substitute import generate_substitution, SubstitutionParams


# One technique to check for password robustness is to run them against dictionaries.

class PasswordDictionary:
    """
    contains a list of words to be checked upon.
    Thses words must have already be substitutes
    """
    name: str
    words: set

    def __init__(self, name, words):
        self.name = name
        self.words = set(words)

    def __repr__(self):
        return f'{self.name} {len(self.words)} words'

    def contains(self, password: str):
        """
        Check if the given password exist in the dictionary
        :param password: the password to check
        :type password: str
        :return: True if it was found
        :rtype: bool

        >>> dico = PasswordDictionary('test', ['flap', 'la', 'girafe'])
        >>> dico.contains('paf')
        False
        >>> dico.contains('girafe')
        True
        """

        return password in self.words


def load_dictionary(filename: str, params: SubstitutionParams):
    """
    Load all the word (one per line) from a text file into a PasswordDictionary.
    Words are trimmed and substitution or character, as well as appending punctuation and and number can be generated

    :param params: specifies the search space when building the dictionary
    :type params: SubstitutionParams
    :param filename: the dictionary file
    :type filename: str
    :return: the loaded dictionary with its words and filename as name
    :rtype: PasswordDictionary
    """
    f = open(filename, "r")
    words = [generate_substitution(w.strip(), params)
             for w in list(f)]
    f.close()
    return PasswordDictionary(filename, list(chain(*words)))


class DictionaryChecker:
    """
    Manages a list of dictionaries
    """

    def __init__(self):
        self.dictionaries = []
        pass

    def __str__(self):
        return f'{len(self.dictionaries)} dictionaries\n' + '\n'.join([str(d) for d in self.dictionaries])

    def load_all_dictionaries(self, dirname: str, params: SubstitutionParams):
        from os import listdir
        files = listdir(dirname)
        for filename in files:
            dico = load_dictionary(f'{dirname}/{filename}', params)
            print(f'Loaded dictionary {dico}')
            self.dictionaries.append(dico)

    def contains(self, password: str):
        """
        Check if the given password exist in any of the dictionaries
        :param password: the password to check
        :type password: str
        :return: True if it was found
        :rtype: bool

        >>> dicoChecker = DictionaryChecker()
        >>> dicoChecker.dictionaries = [PasswordDictionary('flap', ['flap', 'la', 'girafe']),PasswordDictionary('paf', ['paf', 'le', 'chien'])]
        >>> dicoChecker.contains('42' )
        False
        >>> dicoChecker.contains('la' )
        True
        >>> dicoChecker.contains('paf')
        True
        """

        for dictionary in self.dictionaries:
            if dictionary.contains(password):
                return True

        return False
