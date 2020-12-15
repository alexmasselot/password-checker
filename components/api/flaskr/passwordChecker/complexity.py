import string


def password_length_score(password: str):
    """
    Get a score based on the password length (source ???)

    :param password: password string
    :type password: str
    :return: a value between 0 and 100
    :rtype: int

    >>> password_length_score('')
    0
    >>> password_length_score('1234')
    0
    >>> password_length_score('123456789')
    32
    >>> password_length_score('12345678901234567890')
    100
    """
    # list of (len, score), sorted by len. We'll stop at the first one when the length is matching
    score_thresholds = [(5, 0), (8, 16), (10, 32), (12, 48), (16, 64), (20, 80)]

    password_length = len(password)
    matching_threshold = next((st for st in score_thresholds if password_length < st[0]), None)
    if matching_threshold is None:
        score = 100
    else:
        score = matching_threshold[1]

    return score


_character_types = {
    'numbers': set('0123456789'),
    'lowercase_chars': set('abcdefghijklmnopqrstuvwxyz'),
    'lowercase_accented': set('éèêëïîùüöçà'),
    'punctuation': set(string.punctuation + ' ')
}
_character_types['uppercase_chars'] = {x.upper() for x in _character_types['lowercase_chars']}
_character_types['uppercase_accented'] = {x.upper() for x in _character_types['lowercase_accented']}


def get_char_type(char: str):
    """
    Get the char type ('numbers', 'lowercase_chars', ...)
    :param char: a single character
    :type char: str
    :return: the char type
    :rtype: str
    >>> get_char_type('4')
    'numbers'
    >>> get_char_type('a')
    'lowercase_chars'
    >>> get_char_type('A')
    'uppercase_chars'
    >>> get_char_type('à')
    'lowercase_accented'
    >>> get_char_type('Î')
    'uppercase_accented'
    >>> get_char_type('{')
    'punctuation'
    """
    type = next((x for x in _character_types.items() if char in x[1]), None)
    if type is None:
        raise TypeError(f'No type found for char "{char}"')
    return type[0]


def alphabet_size(password: str):
    """
    Get the length of the alphabet, based on the chars in the password
    If it has numbers => 10
    It it has numbers + lowercase => 10 + 26
    It it has numbers + lowercase + uppercase => 10 + 26 + 26
    :param password: the given password
    :type password: str
    :return: the length of the alphabet size
    :rtype: int
    >>> alphabet_size('')
    0
    >>> alphabet_size('42')
    10
    >>> alphabet_size('paf')
    26
    >>> alphabet_size('PAF')
    26
    >>> alphabet_size('pafPAF42')
    62
    """

    # get the unique char types ({} set notation)
    chars_types = {get_char_type(c) for c in password}

    return sum([len(_character_types[t]) for t in chars_types])


def compute_brute_force_ms(password: str):
    """
    Estimate the time to simply brute force the password

    :param password: the submitted password
    :type password: str
    :return: estimated milliseconds to brute force
    :rtype: int

    >>> compute_brute_force_ms('haha')
    1.4374834853727588e-06
    >>> compute_brute_force_ms('p4F le Chï3n !')
    7.111997344304575e+16
    """
    i7_ips = 317900000000
    return (alphabet_size(password) ** len(password)) / float(i7_ips)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
