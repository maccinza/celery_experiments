from functools import wraps

def memoize(function):
    cache = {}

    @wraps(function)
    def wrapper(*args):
        if args not in cache:
            cache[args] = function(*args)
        return cache[args]
    return wrapper


@memoize
def fibonacci(n):
    if n in [0, 1]:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
