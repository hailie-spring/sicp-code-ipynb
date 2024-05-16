def square(x):
    return x * x


def average(x, y):
    return (x + y) / 2


def cube(x):
    return x * x * x


def good_enough(guess, x):
    return abs(square(guess) - x) < 0.001


def improve_guess(guess, x):
    return average(guess, x / guess)


def sqrt_iter(guess, x):
    if good_enough(guess, x):
        return guess
    return sqrt_iter(improve_guess(guess, x), x)


def sqrt(x):
    return sqrt_iter(1, x)
