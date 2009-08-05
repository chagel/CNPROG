"""Utilities for working with lists and sequences."""

def flatten(x):
    """
    Returns a single, flat list which contains all elements retrieved
    from the sequence and all recursively contained sub-sequences
    (iterables).

    Examples:
    >>> [1, 2, [3, 4], (5, 6)]
    [1, 2, [3, 4], (5, 6)]

    From http://kogs-www.informatik.uni-hamburg.de/~meine/python_tricks
    """
    result = []
    for el in x:
        if hasattr(el, '__iter__') and not isinstance(el, basestring):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result

def batch_size(items, size):
    """
    Retrieves items in batches of the given size.

    >>> l = range(1, 11)
    >>> batch_size(l, 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]
    >>> batch_size(l, 5)
    [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]
    """
    return [items[i:i+size] for i in xrange(0, len(items), size)]

def batches(items, number):
    """
    Retrieves items in the given number of batches.

    >>> l = range(1, 11)
    >>> batches(l, 1)
    [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]
    >>> batches(l, 2)
    [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]
    >>> batches(l, 3)
    [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10]]
    >>> batches(l, 4)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]
    >>> batches(l, 5)
    [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]

    Initial batches will contain as many items as possible in cases where
    there are not enough items to be distributed evenly.

    >>> batches(l, 6)
    [[1, 2], [3, 4], [5, 6], [7, 8], [9], [10]]
    >>> batches(l, 7)
    [[1, 2], [3, 4], [5, 6], [7], [8], [9], [10]]
    >>> batches(l, 8)
    [[1, 2], [3, 4], [5], [6], [7], [8], [9], [10]]
    >>> batches(l, 9)
    [[1, 2], [3], [4], [5], [6], [7], [8], [9], [10]]
    >>> batches(l, 10)
    [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]

    If there are more batches than items, empty batches will be appended
    to the batch list.

    >>> batches(l, 11)
    [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10], []]
    >>> batches(l, 12)
    [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [], []]
    """
    div, mod= divmod(len(items), number)
    if div > 1:
        if mod:
            div += 1
        return batch_size(items, div)
    else:
        if not div:
            return [[item] for item in items] + [[]] * (number - mod)
        elif div == 1 and not mod:
            return [[item] for item in items]
        else:
            # mod now tells you how many lists of 2 you can fit in
            return ([items[i*2:(i*2)+2] for i in xrange(0, mod)] +
                    [[item] for item in items[mod*2:]])
