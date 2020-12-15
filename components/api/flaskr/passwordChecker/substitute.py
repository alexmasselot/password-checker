from itertools import product, chain
import re


# if a word such as 'bonjour' is passed, we want to check variants, by substituting letters, adding punctuation and
# so on. This file contains the function to check on the fly all those variants

class ScramblingParams:
    def __init__(self,
                 max_trailing: int = 0,
                 trailing_numbers: bool = True,
                 trailing_punctuations: bool = True
                 ):
        """
        Defines the space to look for when we scan for scrambled passwords
        :param max_trailing: what is the length of the trail to wipe if it is either punctuation or numbers [0]
        :type max_trailing: int
        :param trailing_numbers: should we be tolerant to trailing numbers [True]
        :type trailing_numbers: bool
        :param trailing_punctuations: should we be tolerant to trailing punctuation characters [True]
        :type trailing_punctuations: bool


        """
        self.trailing_numbers = trailing_numbers
        self.trailing_punctuations = trailing_punctuations
        self.max_trailing = max_trailing


_sub_dict = {
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

_punctuation = ['!', '@', '#', '$', '%', '^', '&', '*', '?']
_numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


class CharacterProjector:
    def __init__(self, subst_dict=_sub_dict, scrambling_params: ScramblingParams = ScramblingParams()
                 ):
        """
        :param subst_dict: a dictionary with the character substitution
        :type subst_dict: dict
        :param scrambling_params: defining the scrambling space
        :type scrambling_params: ScramblingParams
        """

        self.scrambling_params = scrambling_params
        self.character_projection = CharacterProjector.build_character_projection(subst_dict)
        self.trailing_regexp = self.build_trailing_regexp()

        self.trailing_cleaning_regexp = CharacterProjector.build_regexp(_numbers + _punctuation, is_tail=True)

    def index_password(self, password: str):
        """
        From an index, generate the ones to be indexed and later searched against.
        Remove ending punctuation and numbers
        :param password: the original password
        :type password: str
        :return: the list of string to index
        :rtype: list[str]

        >>> CharacterProjector().index_password('paf')
        ['paf']
        >>> CharacterProjector().index_password('Paf')
        ['paf']
        >>> CharacterProjector().index_password('hello')
        ['heiio']
        >>> CharacterProjector().index_password('he6a')
        ['heba', 'hega']
        """
        cleaned_up = self.trailing_cleaning_regexp.sub('', password)
        return self.project_word(cleaned_up)

    def potential_indexes(self, password: str):
        """
        Based on a submitted password, generate the one that might have been indexed
        :param password:
        :type password:
        :return:
        :rtype:
        >>> CharacterProjector().potential_indexes('HE!io')
        ['heiio']
        >>> CharacterProjector(scrambling_params=ScramblingParams(max_trailing=2)).potential_indexes('HeL101234')
        ['heiioiz', 'heiiqiz', 'heiioize', 'heiiqize', 'heiioizea', 'heiiqizea']
        >>> CharacterProjector(scrambling_params=ScramblingParams(max_trailing=10)).potential_indexes('HeL101234')
        ['hei', 'heii', 'heiio', 'heiiq', 'heiioi', 'heiiqi', 'heiioiz', 'heiiqiz', 'heiioize', 'heiiqize', 'heiioizea', 'heiiqizea']
        >>> CharacterProjector(scrambling_params=ScramblingParams(max_trailing=2)).potential_indexes('HE!io__')
        ['heiio__']
        """

        if self.trailing_regexp:
            m = self.trailing_regexp.search(password)
            if m:
                truncated_passwords = [password[0:i] for i in range(m.start(), m.end() + 1)]
                return list(chain(*[self.project_word(p) for p in truncated_passwords]))

        return self.project_word(password)

    def trim(self, word):
        """

        :param word:
        :type word:
        :return:
        :rtype:
        >>> CharacterProjector({'q': ['q', '9'], 'g': ['g', '6', '9']}).trim('paf')
        'paf'
        >>> CharacterProjector({'q': ['q', '9'], 'g': ['g', '6', '9']}).trim('pa9')
        'pa9'
        """
        return word

    def project_word(self, word):
        """
        Project the given word towards the combinaison (typically of lowercase characted)
        :param word: the original word, typically a scrambled password
        :type word: str
        :return: the list of possibilities
        :rtype: list[str]
        >>> CharacterProjector({'q': ['q', '9'], 'g': ['g', '6', '9']}).project_word('paf')
        ['paf']
        >>> CharacterProjector({'q': ['q', '9'], 'g': ['g', '6', '9']}).project_word('p!af')
        ['p!af']
        >>> CharacterProjector({'q': ['q', '9'], 'g': ['g', '6', '9']}).project_word('pa6')
        ['pag']
        >>> CharacterProjector({'q': ['q', '9'], 'g': ['g', '6', '9']}).project_word('pa9')
        ['pag', 'paq']
        >>> CharacterProjector({'q': ['q', '9'], 'g': ['g', '6', '9']}).project_word('pa99')
        ['pagg', 'pagq', 'paqg', 'paqq']
        """
        combinatorial = [self.project_char(c) for c in word]
        return [''.join(c) for c in product(*combinatorial)]

    def project_char(self, char):
        """
        return the array of the projected char, or a singleton if no projection is registered
        :return: the list of chars
        :rtype: list[str]
        >>> CharacterProjector({'q': ['q', '9'], 'g': ['g', '6', '9']}).project_char('6')
        ['g']
        >>> CharacterProjector({'q': ['q', '9'], 'g': ['g', '6', '9']}).project_char('9')
        ['g', 'q']
        >>> CharacterProjector({'q': ['q', '9'], 'i': ['i', 'I', '1', 'l', 'L', '|', '!'], 'l': ['l', 'L', 'i', 'I', '|', '!', '1']}).project_char('9')
        ['q']
        >>> CharacterProjector({'q': ['q', '9'], 'i': ['i', 'I', '1', 'l', 'L', '|', '!'], 'l': ['l', 'L', 'i', 'I', '|', '!', '1']}).project_char('I')
        ['i']
        >>> CharacterProjector({'q': ['q', '9'], 'i': ['i', 'I', '1', 'l', 'L', '|', '!'], 'l': ['l', 'L', 'i', 'I', '|', '!', '1']}).project_char('L')
        ['i']
        >>> CharacterProjector({'q': ['q', '9'], 'i': ['i', 'I', '1', 'l', 'L', '|', '!'], 'l': ['l', 'L', 'i', 'I', '|', '!', '1']}).project_char('!')
        ['i']
        >>> CharacterProjector({'q': ['q', '9'], 'g': ['g', '6', '9']}).project_char('?')
        ['?']
        >>> CharacterProjector().project_char('L')
        ['i']
        """
        return self.character_projection.get(char, [char])

    def build_trailing_regexp(self):
        """
        Build the regular expression that is able to catch the trailing number/punctuation, depending on
        the CharacterProjector properties
        :return: the regular expression to capture what is eventually to be trimmed. Or None
        :rtype: Regexp
        >>> proj = CharacterProjector(scrambling_params=ScramblingParams(max_trailing=0, trailing_punctuations=True, trailing_numbers=True))
        >>> proj.build_trailing_regexp()

        >>> proj = CharacterProjector(scrambling_params=ScramblingParams(max_trailing=2, trailing_punctuations=True, trailing_numbers=True))
        >>> proj.build_trailing_regexp().sub('', 'abcdef1!4?')
        'abcdef1!'
        >>> proj = CharacterProjector(scrambling_params=ScramblingParams(max_trailing=8, trailing_punctuations=True, trailing_numbers=True))
        >>> proj.build_trailing_regexp().sub('', 'abcdef1!4?')
        'abcdef'
        """
        if self.scrambling_params.max_trailing > 0:
            if self.scrambling_params.trailing_numbers:
                if self.scrambling_params.trailing_punctuations:
                    trailing_chars = _punctuation + _numbers
                else:
                    trailing_chars = _numbers
            else:
                if self.scrambling_params.trailing_punctuations:
                    trailing_chars = _numbers
            return CharacterProjector.build_regexp(trailing_chars, is_tail=True,
                                                   max_length=self.scrambling_params.max_trailing)
        return None

    @staticmethod
    def build_regexp(chars: list, is_not: bool = False, is_head: bool = False, is_tail: bool = False,
                     max_length: int = 0):
        """
        Create a rgular expression matchin a list opf characters
        :param chars: the list of matchin gcharacters
        :type chars: list[str]
        :param is_not: match everything but the list [False]
        :type is_head: bool
        :param is_head: is the regular expression anchor to the beginning [False]
        :type is_head: bool
        :param is_tail: is the regular expression anchored to the tail [False]
        :type is_tail: bool
        :param max_length: max pattern length. 0 means unlimited [0]
        :type max_length: int
        :return: a regular expression
        :rtype: Regex
        >>> CharacterProjector.build_regexp(['0', '1', '2']).sub('', 'abc')
        'abc'
        >>> CharacterProjector.build_regexp(['0', '1', '2']).sub('', 'abc12')
        'abc'
        >>> CharacterProjector.build_regexp(['0', '1', '2']).sub('', 'abc9322')
        'abc93'
        >>> CharacterProjector.build_regexp(['0', '1', '2'], max_length=3, is_tail=True).sub('', 'abc930221')
        'abc930'
        >>> CharacterProjector.build_regexp(['0', '1', '2']).sub('', 'abc9129')
        'abc99'
        >>> CharacterProjector.build_regexp(['0', '1', '2'], is_not=True).sub('', 'abc')
        ''
        >>> CharacterProjector.build_regexp(['0', '1', '2'], is_not=True).sub('', '123abc2')
        '122'
        >>> CharacterProjector.build_regexp(['0', '1', '2'], is_not=True, is_tail=True).sub('', '123abc2')
        '123abc2'
        >>> CharacterProjector.build_regexp(['0', '1', '2'], is_tail=True).sub('', 'abc9129')
        'abc9129'
        >>> CharacterProjector.build_regexp(['0', '1', '2'], is_head=True).sub('', '123abc9129')
        '3abc9129'
        >>> CharacterProjector.build_regexp(['0', '1', '2'], is_head=True, is_tail=True).sub('', '123abc9129')
        '123abc9129'
        >>> CharacterProjector.build_regexp(['0', '1', '2'], is_head=True, is_tail=True).sub('', '012210')
        ''
        >>> CharacterProjector.build_regexp(['(', ')', '{', '}', '.', '?', '!', '+', '^', '$']).sub('', 'abc(){}.?+^$')
        'abc'
        """
        regexp_special_character = {'(', ')', '{', '}', '[', ']', '.', '?', '!', '^', '$', '\\'}
        str_regexp = ''.join(['\\' + c for c in chars if c in regexp_special_character] + [c for c in chars if
                                                                                           c not in regexp_special_character])

        if is_not:
            str_regexp = '^' + str_regexp
        str_regexp = f'[{str_regexp}]'
        if max_length:
            str_regexp += '{1,' + str(max_length) + '}'
        else:
            str_regexp += '+'
        if is_tail:
            str_regexp += '$'
        if is_head:
            str_regexp = '^' + str_regexp
        return re.compile(str_regexp)

    @staticmethod
    def build_character_projection(subst_dict: dict):
        """
        from a substDict, build the project (the reverse one)
        :param subst_dict: one letter can be replace by several (char -> list of chars)
        :type subst_dict: dict
        :return: the projection (char -> list of chars
        :rtype: dict
        >>> # a single entry
        >>> CharacterProjector.build_character_projection({'a': ['a', 'A', '@']})
        {'a': ['a'], 'A': ['a'], '@': ['a']}
        >>> # two non overlapping entries
        >>> CharacterProjector.build_character_projection({'a': ['a', 'A', '@'], 'b': ['b', 'B', '8', '6']})
        {'a': ['a'], 'A': ['a'], '@': ['a'], 'b': ['b'], 'B': ['b'], '8': ['b'], '6': ['b']}
        >>> # i/l project to the same
        >>> CharacterProjector.build_character_projection({'i': ['i', 'I', '1', 'l', 'L', '|', '!'], 'l': ['i', 'I', '1', 'l', 'L', '|', '!']})
        {'i': ['i'], 'I': ['i'], '1': ['i'], 'l': ['i'], 'L': ['i'], '|': ['i'], '!': ['i']}
        >>> # q/g share 9, but not 6
        >>> CharacterProjector.build_character_projection({'q': ['q', 'Q', '9', '0', 'O'], 'g': ['g', 'G', '6', '9']})
        {'g': ['g'], 'G': ['g'], '6': ['g'], '9': ['g', 'q'], 'q': ['q'], 'Q': ['q'], '0': ['q'], 'O': ['q']}
        """
        proj_set = {}
        seen_projections = set()
        for char_root, subst in sorted(subst_dict.items(), key=lambda k: k[0]):
            subst_str = ''.join(sorted(subst))
            if subst_str in seen_projections:
                continue
            seen_projections.add(subst_str)
            for char_subst in subst:
                if char_subst not in proj_set:
                    proj_set[char_subst] = set()
                proj_set[char_subst].add(char_root)
        return {k: sorted(list(xs)) for k, xs in proj_set.items()}
