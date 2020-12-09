class PasswordDictionary:
    name: str
    words: set

    def __init__(self, name, words):
        self.name = name
        self.words = set(words)


def exists_in_dictionary(password: str, dictionary: PasswordDictionary):
    """
    Check if the given password exist in the dictionary
    :param password: the password to check
    :type password: str
    :param dictionary: a dictionary where to look into
    :type dictionary: PasswordDictionary
    :return: True if it was found
    :rtype: bool

    >>> exists_in_dictionary('paf', PasswordDictionary('test', ['flap', 'la', 'girafe']))
    False
    >>> exists_in_dictionary('girafe', PasswordDictionary('test', ['flap', 'la', 'girafe']))
    True
    """

    return password in dictionary.words


def exists_in_any_dictionary(password: str, dictionaries: list):
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
