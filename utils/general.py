import itertools

def flatten(list_of_lists):
    return list(itertools.chain.from_iterable(list_of_lists))
