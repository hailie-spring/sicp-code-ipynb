def cons(x, y):
    def set_x(v):
        nonlocal x
        x = v

    def set_y(v):
        nonlocal y
        y = v

    def dispatch(name):
        match name:
            case "car":
                return x
            case "cdr":
                return y
            case "set_car":
                return set_x
            case "set_cdr":
                return set_y

        raise Exception("unsupported name: %s" % (name))

    return dispatch


def car(z):
    return z("car")


def cdr(z):
    return z("cdr")


def caar(z):
    return car(car(z))


def cdar(z):
    return cdr(car(z))


def cadr(z):
    return car(cdr(z))


def set_car(z, new_value):
    z("set_car")(new_value)
    return z


def set_cdr(z, new_value):
    z("set_cdr")(new_value)
    return z


def list(*args):
    if args == ():
        return None
    return cons(args[0], list(*args[1:]))


def display_list(lst):

    def sub_display_list(lst):
        if lst is None:
            return ""
        if not callable(lst):
            return str(lst) + " "
        if callable(car(lst)):
            return "( " + sub_display_list(car(lst)) + ") " + sub_display_list(cdr(lst))
        return sub_display_list(car(lst)) + sub_display_list(cdr(lst))

    text = sub_display_list(lst)
    print("( " + text + ")")


def enumerate_interval(start, end):
    if start > end:
        return None
    return cons(start, enumerate_interval(start + 1, end))


def map(proc, tree):
    if tree is None:
        return None
    return cons(proc(car(tree)), map(proc, cdr(tree)))


def filter(proc, seqs):
    if seqs is None:
        return None
    if proc(car(seqs)):
        return cons(car(seqs), filter(proc, cdr(seqs)))
    return filter(proc, cdr(seqs))


def append(x1, x2):
    if x1 is None:
        return x2
    return cons(car(x1), append(cdr(x1), x2))


def accumulate(op, initial, sequence):
    if sequence is None:
        return initial
    return op(car(sequence), accumulate(op, initial, cdr(sequence)))

def flatmap(seq):
    return accumulate(append, None, seq)

def square(x):
    return x * x


def cube(x):
    return x * x * x


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

def equal(lst1, lst2):
    if lst1 is None and lst2 is None:
        return True
    if lst1 is None or lst2 is None:
        return False
    if not callable(car(lst1)) and not callable(car(lst2)):
        if car(lst1) == car(lst2):
            return equal(cdr(lst1), cdr(lst2))
        return False
    if callable(car(lst1)) and callable(car(lst2)):
        return equal(car(lst1), car(lst2)) and equal(cdr(lst1), cdr(lst2))
    return False

