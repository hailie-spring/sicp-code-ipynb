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

def next_odd(x):
    if x % 2 == 0:
        return x + 1
    return x + 2

def next_tester(x):
    return x + 1

def smallest_divisor(n):
    def find_divisor(n, test_divisor):
        if square(test_divisor) > n:
            return n
        if n % test_divisor == 0:
            return test_divisor
        return find_divisor(n, next_tester(test_divisor))
    return find_divisor(n, 2)

def is_prime(n):
    if smallest_divisor(n) == n:
        return True
    return False