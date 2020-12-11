def length_score(password: str):
    """
    Get a score based on the password length (source ???)

    :param password: password string
    :type password: str
    :return: a value between 0 and 100
    :rtype: int

    >>> length_score('')
    0
    >>> length_score('1234')
    0
    >>> length_score('123456789')
    32
    >>> length_score('12345678901234567890')
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


def brute_force_ms(password: str):
    """
    Estimate the time to simply brute force the password

    :param password: the submitted password
    :type password: str
    :return: estimated milliseconds to brute force
    :rtype: int

    >>> brute_force_ms('haha')
    40
    """
    return 10 * len(password)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
