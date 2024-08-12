function stream_tail(stream) {
    return tail(stream)();
}

function stream_ref(s, n) {
    return n === 0
        ? head(s)
        : stream_ref(stream_tail(s), n - 1);
}
function stream_map(f, s) {
    return is_null(s)
        ? null
        : pair(f(head(s)),
            () => stream_map(f, stream_tail(s)));
}
function stream_for_each(fun, s) {
    if (is_null(s)) {
        return true;
    } else {
        fun(head(s));
        return stream_for_each(fun, stream_tail(s));
    }
}

function pair(x, y) {
    function dispatch(m) {
        return m === 0
            ? x
            : m === 1
                ? y
                : error(m, "argument not 0 or 1 -- pair");
    }
    return dispatch;
}
function head(z) { return z(0); }

function tail(z) { return z(1); }

const display = console.log

function is_null(s) {
    return s === null;
}

const max_display = 9;
function display_stream(s) {
    function display_stream_iter(st, n) {
        if (is_null(st)) {
        } else if (n === 0) {
            display('', "...");
        } else {
            display(head(st));
            display_stream_iter(stream_tail(st), n - 1);
        }
    }
    display_stream_iter(s, max_display);
}

function average(x, y) {
    return (x + y) / 2;
}

function sqrt_improve(guess, x) {
    return average(guess, x / guess);
}

function sqrt_stream(x) {
   return pair(1, () => stream_map(guess => sqrt_improve(guess, x),
                                   sqrt_stream(x)));
}

display_stream(sqrt_stream(2));
