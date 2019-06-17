import sys


def warning(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def filter_arff(file_list):
    return list(filter(lambda x: x.endswith('.arff'), file_list))

class InconsistentError(Exception):
    pass
