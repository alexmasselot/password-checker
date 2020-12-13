from itertools import product, chain, combinations


class SubstitutionParams:
    substitute_characters: int
    append_punctuation: bool
    append_number: bool

    def __init__(self,
                 substitute_characters: int = 10000,
                 append_punctuation: bool = False,
                 append_number: bool = False
                 ):
        """
        Defines the space to looks for when we build a dictionary
        :param substitute_characters: should we run the character substitution [10000 => all]
        :type substitute_characters: bool
        :param append_punctuation: should we append number to each substitution [False]
        :type append_punctuation:
        :param append_number: should we append number to each substitution [False]
        :type append_number: bool

        """
        self.substitute_characters = substitute_characters
        self.append_punctuation = append_punctuation
        self.append_number = append_number


_subDict = {
    'a': ['a', 'A', '@', '4'],
    'b': ['b', 'B', '8', '6'],
    'c': ['c', 'C', '[', '{', '(', '<'],
    'd': ['d', 'D', ],
    'e': ['e', 'E', '3'],
    'f': ['f', 'F'],
    'g': ['g', 'G', '6', '9'],
    'h': ['h', 'H', '#'],
    'i': ['i', 'I', '1', 'l', 'L', '|', '!'],
    'j': ['j', 'J'],
    'k': ['k', 'K'],
    'l': ['l', 'L', 'i', 'I', '|', '!', '1'],
    'm': ['m', 'M'],
    'n': ['n', 'N'],
    'o': ['o', 'O', '0', 'Q'],
    'p': ['p', 'P'],
    'q': ['q', 'Q', '9', '0', 'O'],
    'r': ['r', 'R'],
    's': ['s', 'S', '$', '5'],
    't': ['t', 'T', '+', '7'],
    'u': ['u', 'U', 'v', 'V'],
    'v': ['v', 'V', 'u', 'U'],
    'w': ['w', 'W'],
    'x': ['x', 'X', '+'],
    'y': ['y', 'Y'],
    'z': ['z', 'Z', '2'],
}
for it in list(_subDict.items()):
    for char in it[1]:
        _subDict[char] = _subDict[it[0]]

_punctuation = ['!', '@', '#', '$', '%', '^', '&', '*', '?']
_numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


def generate_substitution(password: str, params: SubstitutionParams):
    """
    Generate all "char subsitution" password (e.g. 'c' -> 'C', 'e' -> '3' etc.)
    :param password: the password to run
    :type password: str
    :param params:
    :type params:
    :return: the list of subsituted password
    :rtype: list[str]

    >>> generate_substitution('paf', SubstitutionParams(substitute_characters=0))
    ['paf']
    >>> generate_substitution('paf', SubstitutionParams(substitute_characters=False, append_number=True))
    ['paf', 'paf0', 'paf1', 'paf2', 'paf3', 'paf4', 'paf5', 'paf6', 'paf7', 'paf8', 'paf9']
    >>> generate_substitution('x', SubstitutionParams())
    ['x', 'X', '+']
    >>> generate_substitution('X', SubstitutionParams())
    ['x', 'X', '+']
    >>> generate_substitution('+', SubstitutionParams())
    ['x', 'X', '+']
    >>> generate_substitution('xX', SubstitutionParams())
    ['xx', 'xX', 'x+', 'Xx', 'XX', 'X+', '+x', '+X', '++']
    >>> generate_substitution('paf', SubstitutionParams())
    ['paf', 'paF', 'pAf', 'pAF', 'p@f', 'p@F', 'p4f', 'p4F', 'Paf', 'PaF', 'PAf', 'PAF', 'P@f', 'P@F', 'P4f', 'P4F']
    >>> [ x for x in generate_substitution('+', SubstitutionParams(append_punctuation=True)) if '#' in x]
    ['x#', 'X#', '+#']
    >>> [ x for x in generate_substitution('+', SubstitutionParams(append_punctuation=True)) if len(x) == 1]
    ['x', 'X', '+']
    >>> [ x for x in generate_substitution('+', SubstitutionParams(append_number=True)) if '4' in x]
    ['x4', 'X4', '+4']
    >>> [ x for x in generate_substitution('+', SubstitutionParams(append_number=True)) if len(x) == 1]
    ['x', 'X', '+']
    >>> [ x for x in generate_substitution('+', SubstitutionParams(append_punctuation=True, append_number=True)) if '#' in x and '4' in x]
    ['x#4', 'X#4', '+#4', 'x4#', 'X4#', '+4#']
    >>> [ x for x in generate_substitution('+', SubstitutionParams(append_punctuation=True, append_number=True)) if '#' in x and len(x)==2]
    ['x#', 'X#', '+#']
    """
    substitutes_orig = substitute_characters(password, params.substitute_characters)

    if params.append_punctuation and params.append_number:
        substitutes = substitutes_orig + [''.join(item) for item in
                                          list(product(*[substitutes_orig, _punctuation])) +
                                          list(product(*[substitutes_orig, _numbers])) +
                                          list(product(*[substitutes_orig, _punctuation, _numbers])) +
                                          list(product(*[substitutes_orig, _numbers, _punctuation]))
                                          ]
    else:
        substitutes = substitutes_orig
        if params.append_punctuation:
            substitutes = substitutes_orig + [''.join(item) for item in
                                              product(*[substitutes_orig, _punctuation])]

        if params.append_number:
            substitutes = substitutes_orig + [''.join(item) for item in
                                              product(*[substitutes_orig, _numbers])]
    return substitutes


def substitute_characters(password: str, nb_chars_to_substitute: int):
    """
    Given a list of passwords, generate a list of passwords by substituting at most a given number of characters
    :param password: the original password
    :type password: str
    :param nb_chars_to_substitute: the number of characters to substitute
    :type nb_chars_to_substitute: int
    :return: the original password
    :rtype: str

    >>> substitute_characters('paf', 0)
    ['paf']
    >>> substitute_characters('paf', 1)
    ['paf', 'Paf', 'pAf', 'p@f', 'p4f', 'paF']
    >>> substitute_characters('paf', 2)
    ['paf', 'Paf', 'pAf', 'p@f', 'p4f', 'paF', 'PAf', 'P@f', 'P4f', 'PaF', 'pAF', 'p@F', 'p4F']
    """
    if nb_chars_to_substitute == 0:
        return [password]

    indexes = list(range(0, len(password)))
    max_substitution = min(nb_chars_to_substitute, len(password))
    substituted_passwords = [password]
    for n_substitution in range(1, max_substitution + 1):
        substitution_indexes = combinations(indexes, n_substitution)
        for index_set in substitution_indexes:
            tmp = list(substitute_character_at_in_list([password], index_set[0]))
            for i in index_set[1:len(index_set) - 1]:
                tmp = tmp + list(substitute_character_at_in_list(tmp, i))
            if len(index_set) > 1:
                substituted_passwords = substituted_passwords + list(
                    substitute_character_at_in_list(tmp, index_set[-1]))
            else:
                substituted_passwords = substituted_passwords + tmp

    return substituted_passwords


def substitute_character_at_in_list(passwords: list, position: int):
    """
    Given a list of passwords, substitute the character at a given position and return the original list + the new one
    :param passwords: the list of passwords. All of them should have the same length
    :type passwords: list[str]
    :param position: which character to substitute
    :type position: int
    :return: the enriched list of characters
    :rtype: Iterable[str]
    """"""
    >>> list(substitute_character_at_in_list(['paf'], 0))
    ['Paf']
    >>> list(substitute_character_at_in_list(['paf', 'fla'], 0))
    ['Paf', 'Fla']
    """

    return chain(*[substitute_character_at(password, position) for password in passwords])


def substitute_character_at(password: str, position: int):
    """
    Given a password, substitute the character at a given position. Only create new passwords
    :param password: the original password
    :type password: str
    :param position: which character to substitute
    :type position: int
    :return: the enriched list of characters
    :rtype: list[str]
    """"""
    >>> substitute_character_at('paf', 0)
    ['Paf']
    >>> substitute_character_at('paf', 1)
    ['pAf', 'p@f', 'p4f']
    >>> substitute_character_at('paf', 2)
    ['paF']
    >>> substitute_character_at('_af', 0)
    []
    """

    if position >= len(password):
        raise ValueError(f'position {position} is out of range for "{password}"')

    char_to_substitute = password[position]
    if char_to_substitute not in _subDict:
        return []

    if position == 0:
        prefix = ''
    else:
        prefix = password[0: position]

    if position == len(password) - 1:
        suffix = ''
    else:
        suffix = password[(position + 1):len(password)]

    return [prefix + subst + suffix for subst in _subDict[char_to_substitute] if subst != char_to_substitute]
