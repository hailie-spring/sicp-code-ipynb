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


