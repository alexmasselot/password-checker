from passwordChecker.complexity import password_length_score, compute_brute_force_ms, alphabet_size
from passwordChecker.dictionary import DictionaryChecker


class PasswordRobustness:
    """
    Manages the various metrics to assess a password robustness
    """
    length_score: int
    brute_force_ms: float
    exists_in_dictionary: bool
    alphabet_size: int

    def __init__(self, length_score: int, brute_force_ms: float, exists_in_dictionary: bool, alphabet_size: int):
        self.length_score = length_score
        self.brute_force_ms = brute_force_ms
        self.exists_in_dictionary = exists_in_dictionary
        self.alphabet_size = alphabet_size

    def serialize(self):
        return {
            "lengthScore": self.length_score,
            "bruteForceMs": self.brute_force_ms,
            "existsInDictionary": self.exists_in_dictionary,
            "alphabetSize": self.alphabet_size
        }


def compute_robustness(password: str, dictionaryChecker: DictionaryChecker):
    """
    aggregates the differents robustness measures
    :param dictionaryChecker: to check of the word exist in some dicitonaries
    :type dictionaryChecker: DictionaryChecker
    :param password: the password to analyze
    :type password: str
    :return: the robustess structure
    :rtype: PasswordRobustness
    """
    return PasswordRobustness(
        length_score=password_length_score(password),
        brute_force_ms=compute_brute_force_ms(password),
        exists_in_dictionary=dictionaryChecker.contains(password),
        alphabet_size=alphabet_size(password)
    )


def level_robustness(passwordRobustness: PasswordRobustness):
    """

    define the level of the password robustness
    :param passwordRobustness: to define the level of the password robustness
    :type passwordRobustness: PasswordRobustness
    :return: the level of the password robustness
    :rtype: int
    level== 1:very_weak, 2:weak, 3:medium, 4:strong
    """
    
    # list of (length_score, key_length)
    key_length_thresholds = [(16, 1), (32, 2), (64, 3), (100, 4)]
    # list of (alphabet_score, key_alphabet)
    key_alphabet_thresholds = [(26, 1), (36, 2), (52, 3), (62, 4)]
    level = 1
    
    if passwordRobustness.exists_in_dictionary==False:
        matching_key_length_threshold = next((lt for lt in key_length_thresholds if passwordRobustness.length_score <= lt[0]), None)
        key_length = matching_key_length_threshold[1]
        matching_key_alphabet_threshold = next((at for at in key_alphabet_thresholds if passwordRobustness.alphabet_size <= at[0]), None)
        key_alphabet = matching_key_alphabet_threshold[1]
        if key_length < key_alphabet:
            level = key_length
        else:
            level = key_alphabet
            
    return level
