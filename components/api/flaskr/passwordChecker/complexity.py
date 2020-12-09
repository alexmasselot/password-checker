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
    return 10*len(password)



if __name__ == "__main__":
    import doctest
    doctest.testmod()
