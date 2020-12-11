from flaskr.passwordChecker.complexity import password_length_score, brute_force_ms


class PasswordRobustness:
    length_score: int
    brute_force_ms: float

    def __init__(self, length_score: int, brute_force_ms: float):
        self.length_score = length_score
        self.brute_force_ms = brute_force_ms

    def serialize(self):
        return {
            "lengthScore": self.length_score,
            "bruteForceMs": self.brute_force_ms
        }


def compute_robustness(password: str):
    """
    aggregates the differents robustness measures
    :param password: the password to analyze
    :type password: str
    :return: the robustess structure
    :rtype: PasswordRobustness
    """
    return PasswordRobustness(
        length_score=password_length_score(password),
        brute_force_ms=brute_force_ms(password)
    )
