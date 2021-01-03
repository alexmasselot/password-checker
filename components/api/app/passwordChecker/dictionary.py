from itertools import chain

# One technique to check for password robustness is to run them against dictionaries.
from passwordChecker.substitute import  CharacterProjector


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

    def contains_exact(self, indexed_password: str):
        """
        Check if the given password exist in the dictionary.
        At this stage, the password must have been projected towards the index (Hell0 -> heiio), as the search will be exact
        :param indexed_password: the password to check
        :type indexed_password: str
        :return: True if it was found
        :rtype: bool

        >>> dico = PasswordDictionary('test', ['fiap', 'ia', 'girafe'])
        >>> dico.contains_exact('paf')
        False
        >>> dico.contains_exact('girafe')
        True
        """

        return indexed_password in self.words


class DictionaryChecker:
    """
    Manages a list of dictionaries
    """

    def __init__(self, character_projector: CharacterProjector):
        self.character_projector = character_projector
        self.dictionaries = []

    def __str__(self):
        return f'{len(self.dictionaries)} dictionaries\n' + '\n'.join([str(d) for d in self.dictionaries])

    def load_all_dictionaries(self, dirname: str):
        """
        Loads dictionaries from all the file found in the given directory and index them
        :param dirname: path to search into (no recursion)
        :type dirname: str
        :param character_projector: how to project characters
        :type character_projector: CharacterProjector
        """
        from os import listdir
        files = listdir(dirname)
        for filename in files:
            dico = self.load_dictionary(f'{dirname}/{filename}')
            print(f'Loaded dictionary {dico}')
            self.dictionaries.append(dico)

    def contains(self, password: str):
        """
        Check if the given password exist in any of the dictionaries. Let's remember that the password were indexed
        :param password: the password to check
        :type password: str
        :return: True if it was found
        :rtype: bool

        >>> dicoChecker = DictionaryChecker(CharacterProjector())
        >>> dicoChecker.dictionaries = [PasswordDictionary('flap', ['fiap', 'ia', 'girafe']), PasswordDictionary('paf', ['paf', 'ie', 'chien'])]
        >>> dicoChecker.contains('42' )
        False
        >>> dicoChecker.contains('la' )
        True
        >>> dicoChecker.contains('paf')
        True
        """

        index_to_search = self.character_projector.potential_indexes(password)
        for to_search in index_to_search:
            for dictionary in self.dictionaries:
                if dictionary.contains_exact(to_search):
                    return True

        return False

    def load_dictionary(self, filename: str):
        """
        Load all the word (one per line) from a text file into a PasswordDictionary.
        Words are trimmed and substitution or character, as well as appending punctuation and and number can be generated

        :param filename: the dictionary file
        :type filename: str
        :param character_projector: how to project characters
        :type character_projector: CharacterProjector
        :return: the loaded dictionary with its words and filename as name
        :rtype: PasswordDictionary
        """
        f = open(filename, "r")
        words = [self.character_projector.index_password(w.strip())
                 for w in list(f)]
        f.close()
        return PasswordDictionary(filename, list(chain(*words)))
