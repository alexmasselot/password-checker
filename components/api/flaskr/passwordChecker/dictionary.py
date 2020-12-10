_all_dictionaries = []


def all_dictionaries():
    return _all_dictionaries


class PasswordDictionary:
    name: str
    words: set

    def __init__(self, name, words):
        self.name = name
        self.words = set(words)

    def __repr__(self):
        return f'{self.name} {len(self.words)} words'


def load_dictionary(filename: str):
    """
    Load all the word (one per line) from a text file into a PasswordDictionary.
    Words are trimmed.

    :param filename: the dictiopnary file
    :type filename: str
    :return: the loaded dictionary with its words and filename as name
    :rtype: PasswordDictionary
    """
    f = open(filename, "r")
    words = [w.strip() for w in list(f)]
    f.close()
    return PasswordDictionary(filename, words)


def load_all_dictionaries(dirname: str):
    global _all_dictionaries
    from os import listdir
    files = listdir(dirname)
    _all_dictionaries = [load_dictionary(f'{dirname}/{filename}') for filename in files]

def exists_in_dictionary(password: str, dictionary: PasswordDictionary):
    """
    Check if the given password exist in the dictionary
    :param password: the password to check
    :type password: str
    :param dictionary: a dictionary where to look into
    :type dictionary: PasswordDictionary
    :return: True if it was found
    :rtype: bool

    //>>> exists_in_dictionary('g1rafe', PasswordDictionary('test', ['flap', 'la', 'girafe']))
    //True
    >>> exists_in_dictionary('paf', PasswordDictionary('test', ['flap', 'la', 'girafe']))
    False
    >>> exists_in_dictionary('girafe', PasswordDictionary('test', ['flap', 'la', 'girafe']))
    True
    """

    return password in dictionary.words


def exists_in_any_dictionary(password: str, dictionaries: list = _all_dictionaries):
    """
    Check if the given password exist in any of the dictionaries
    :param password: the password to check
    :type password: str
    :param dictionaries: list of dictionaries where to look into
    :type dictionaries: list[PasswordDictionary]
    :return: True if it was found
    :rtype: bool

    >>> exists_in_any_dictionary('42', [PasswordDictionary('flap', ['flap', 'la', 'girafe']), PasswordDictionary('paf', ['paf', 'le', 'chien'])] )
    False
    >>> exists_in_any_dictionary('la', [PasswordDictionary('flap', ['flap', 'la', 'girafe']), PasswordDictionary('paf', ['paf', 'le', 'chien'])] )
    True
    >>> exists_in_any_dictionary('paf', [PasswordDictionary('flap', ['flap', 'la', 'girafe']), PasswordDictionary('paf', ['paf', 'le', 'chien'])] )
    True
    """

    for dictionary in dictionaries:
        if exists_in_dictionary(password, dictionary):
            return True

    return False
