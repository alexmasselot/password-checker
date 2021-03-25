from passwordChecker.complexity import password_length_score, compute_brute_force_ms
from passwordChecker.dictionary import DictionaryChecker


class PasswordRobustness:
    """
    Manages the various metrics to assess a password robustness
    """
    length_score: int
    brute_force_ms: float
    exists_in_dictionary: bool

    def __init__(self, length_score: int, brute_force_ms: float, exists_in_dictionary: bool):
        self.length_score = length_score
        self.brute_force_ms = brute_force_ms
        self.exists_in_dictionary = exists_in_dictionary

    def serialize(self):
        return {
            "lengthScore": self.length_score,
            "bruteForceMs": self.brute_force_ms,
            "existsInDictionary": self.exists_in_dictionary
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
        exists_in_dictionary=dictionaryChecker.contains(password)
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
    # list of (len_score, level), sorted by len_score. We'll stop at the first one when the length_score is matching
    level_thresholds = [(16, 1), (32, 2), (64, 3), (100, 4)]
    level = 1

    if passwordRobustness.exists_in_dictionary==False:
        matching_threshold = next((lt for lt in level_thresholds if passwordRobustness.length_score <= lt[0]), None)
        level = matching_threshold[1]

    return level
