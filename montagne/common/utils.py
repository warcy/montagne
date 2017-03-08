import sys


def unicode_fmt(i):
    """format unicode object in dict & list to string or int
    only used for python2

    :param i: dict/list object with unicode object
    :return: formatted object
    """
    if sys.version_info[0] >= 3:
        return i

    if isinstance(i, dict):
        return {unicode_fmt(key): unicode_fmt(value)
                for key, value in i.items()}
    elif isinstance(i, list):
        return [unicode_fmt(element) for element in i]
    elif isinstance(i, unicode):
        return i.encode('utf-8')
    elif isinstance(i, int):
        return int(i)
    else:
        return i
