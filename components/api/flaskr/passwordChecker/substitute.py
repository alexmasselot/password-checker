from itertools import product

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


def generate_substitution(password: str, substitute_characters:bool = True, append_punctuation: bool = False, append_number: bool = False):
    """
    Generate all "char subsitution" password (e.g. 'c' -> 'C', 'e' -> '3' etc.)
    :param substitute_characters: Shall we run the character substituion
    :type substitute_characters: bool
    :param append_punctuation: True to append a punctuation character
    :type append_punctuation: bool
    :param append_number: True to append a digit character
    :type append_number: bool
    :param password: the password to run
    :type password: str
    :return: the list of subsituted password
    :rtype: list[str]

    >>> generate_substitution('paf', substitute_characters=False)
    ['paf']
    >>> generate_substitution('paf', substitute_characters=False, append_number=True)
    ['paf', 'paf0', 'paf1', 'paf2', 'paf3', 'paf4', 'paf5', 'paf6', 'paf7', 'paf8', 'paf9']
    >>> generate_substitution('x')
    ['x', 'X', '+']
    >>> generate_substitution('X')
    ['x', 'X', '+']
    >>> generate_substitution('+')
    ['x', 'X', '+']
    >>> generate_substitution('xX')
    ['xx', 'xX', 'x+', 'Xx', 'XX', 'X+', '+x', '+X', '++']
    >>> generate_substitution('paf')
    ['paf', 'paF', 'pAf', 'pAF', 'p@f', 'p@F', 'p4f', 'p4F', 'Paf', 'PaF', 'PAf', 'PAF', 'P@f', 'P@F', 'P4f', 'P4F']
    >>> [ x for x in generate_substitution('+',append_punctuation=True) if '#' in x]
    ['x#', 'X#', '+#']
    >>> [ x for x in generate_substitution('+',append_punctuation=True) if len(x) == 1]
    ['x', 'X', '+']
    >>> [ x for x in generate_substitution('+',append_number=True) if '4' in x]
    ['x4', 'X4', '+4']
    >>> [ x for x in generate_substitution('+',append_number=True) if len(x) == 1]
    ['x', 'X', '+']
    >>> [ x for x in generate_substitution('+',append_punctuation=True,append_number=True) if '#' in x and '4' in x]
    ['x#4', 'X#4', '+#4', 'x4#', 'X4#', '+4#']
    >>> [ x for x in generate_substitution('+',append_punctuation=True,append_number=True) if '#' in x and len(x)==2]
    ['x#', 'X#', '+#']
    """
    if substitute_characters:
        letters = []
        for val in password:
            if val in _subDict.keys():
                letters.append(_subDict[val])
            else:
                letters.append([val])
        substitutes_orig = [''.join(item) for item in product(*letters)]
    else:
        substitutes_orig = [password]

    if append_punctuation and append_number:
        substitutes = substitutes_orig + [''.join(item) for item in
                                          list(product(*[substitutes_orig, _punctuation])) +
                                          list(product(*[substitutes_orig, _numbers])) +
                                          list(product(*[substitutes_orig, _punctuation, _numbers])) +
                                          list(product(*[substitutes_orig, _numbers, _punctuation]))
                                          ]
    else:
        substitutes = substitutes_orig
        if append_punctuation:
            substitutes = substitutes_orig + [''.join(item) for item in
                                              product(*[substitutes_orig, _punctuation])]

        if append_number:
            substitutes = substitutes_orig + [''.join(item) for item in
                                              product(*[substitutes_orig, _numbers])]
    return substitutes
