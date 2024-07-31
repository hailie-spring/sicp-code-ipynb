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
        if arg.__qualname__.startswith("delay"):
            arg = force(arg)
        params.append(car_stream(arg))
        next_stream.append(cdr_stream(arg))
    return cons_stream(proc(*params), delay(map_stream, proc, *next_stream))


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


def last_pair(x):
    if x is None:
        return None
    if cdr(x) is None:
        return x
    return last_pair(cdr(x))


def append_set(x, y):
    set_cdr(last_pair(x), y)
    return x


def append(x, y):
    if x is None:
        return y
    return cons(car(x), append(cdr(x), y))


def make_queue():
    return cons(None, None)


def empty_queue(queue):
    return car(queue) is None


def front_ptr(queue):
    return car(queue)


def rear_ptr(queue):
    return cdr(queue)


def front_queue(queue):
    if empty_queue(queue):
        return None
    return car(front_ptr(queue))


def rear_queue(queue):
    if empty_queue(queue):
        return None
    return car(rear_ptr(queue))


def set_front_ptr(queue, item):
    set_car(queue, item)


def set_rear_ptr(queue, item):
    set_cdr(queue, item)


def insert_queue(queue, value):
    new_pair = cons(value, None)
    if empty_queue(queue):
        set_front_ptr(queue, new_pair)
        set_rear_ptr(queue, new_pair)
    else:
        set_cdr(rear_ptr(queue), new_pair)
        set_rear_ptr(queue, new_pair)
    return queue


def delete_queue(queue):
    if empty_queue(queue):
        return None
    ptr = front_ptr(queue)
    next_item = cdr(ptr)
    set_front_ptr(queue, next_item)
    return queue


def make_deque():
    deque = cons(None, None)

    def empty_deque():
        if car(deque) is None:
            return True
        return False

    def front_ptr():
        return car(deque)

    def rear_ptr():
        return cdr(deque)

    def set_front_ptr(item):
        set_car(deque, item)

    def set_rear_ptr(item):
        set_cdr(deque, item)

    def insert_front_deque(item):
        # Node structure: value, previous_ptr, next_ptr
        ptr = cons(None, None)
        new_node = cons(item, ptr)
        new_pair = cons(new_node, None)
        if empty_queue(deque):
            set_rear_ptr(new_pair)
            set_front_ptr(new_pair)
        else:
            previous_front = car(front_ptr())
            set_car(cdr(previous_front), new_pair)
            set_cdr(ptr, front_ptr())
            set_cdr(new_pair, front_ptr())
            set_front_ptr(new_pair)

    def insert_rear_deque(item):
        # Node structure: value, previous_ptr, next_ptr
        ptr = cons(None, None)
        new_node = cons(item, ptr)
        new_pair = cons(new_node, None)
        previous_rear = car(rear_ptr())
        set_car(ptr, rear_ptr())
        set_cdr(cdr(previous_rear), new_pair)
        set_cdr(rear_ptr(), new_pair)
        if empty_deque():
            set_front_ptr(new_pair)
            set_rear_ptr(new_pair)
        else:
            set_rear_ptr(new_pair)

    def delete_front_deque():
        if empty_deque():
            return None
        front = car(front_ptr())
        next_pair = cdr(front_ptr())
        set_cdr(cdr(front), None)  # release reference, garbage collection
        set_front_ptr(next_pair)
        if next_pair is None:
            set_rear_ptr(next_pair)
        else:
            set_car(cdr(car(next_pair)), None)

    def delete_rear_deque():
        if empty_deque():
            return None
        rear = car(rear_ptr())
        previous = car(cdr(rear))
        set_car(cdr(rear), None)  # release reference, garbage collection
        set_rear_ptr(previous)
        if previous is None:
            set_front_ptr(previous)
        else:
            set_cdr(cdr(car(previous)), None)

    def display_deque():

        def sub_display_deque(deq):
            if deq is None:
                return ""
            node = car(deq)
            return str(car(node)) + " " + sub_display_deque(cdr(cdr(node)))

        text = sub_display_deque(front_ptr())
        print("( " + text + ")")

    def dispatch(name):
        match name:
            case "front_ptr":
                return front_ptr()
            case "rear_ptr":
                return rear_ptr()
            case "delete_front_deque":
                return delete_front_deque()
            case "insert_front_deque":
                return insert_front_deque
            case "delete_rear_deque":
                return delete_rear_deque()
            case "insert_rear_deque":
                return insert_rear_deque
            case "display_deque":
                return display_deque()

    return dispatch
