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


def set_car(z, new_value):
    z("set_car")(new_value)
    return z


def set_cdr(z, new_value):
    z("set_cdr")(new_value)
    return z


def cons_stream(x, y):
    return cons(x, y)


def car_stream(z):
    return z("car")


def cdr_stream(z):
    return force(cdr(z))


def delay(func, *args, **kwargs):

    def sub_func():
        return func(*args, **kwargs)

    return sub_func


def force(func):
    return func()


def filter_stream(proc, s):
    if s is None:
        return None
    if proc(car_stream(s)):
        return cons_stream(car_stream(s), delay(filter_stream, proc, cdr_stream(s)))
    return filter_stream(proc, cdr_stream(s))


def ref_stream(s, n):
    if n == 0:
        return car_stream(s)
    if s is None:
        return None
    return ref_stream(cdr_stream(s), n - 1)

def map_stream(proc, *args):
    params = []
    next_stream = []
    for arg in args:
        if arg is None:
            return
        if arg.__qualname__.startswith('delay'):
            arg = force(arg)
        params.append(car_stream(arg))
        next_stream.append(cdr_stream(arg))
    return cons_stream(proc(*params), delay(map_stream, proc, *next_stream))
