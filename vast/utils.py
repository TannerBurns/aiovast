from typing import NamedTuple


class EventLoopReport(NamedTuple):
    """EventLoopReport - NamedTuple for reporting information gathered before and after the event loop
    """
    function_name: str
    function_docstring: str
    function_hash: str
    function_sha256: str
    input_count: int
    input_sha256: str
    output_count: int
    output_sha256: str
    start_time: int
    stop_time: int
    runtime: int
    results: list


class vast_fragment(object):
    """vast_fragment - simple implementation of functools.partial
    """

    __slots__ = 'fn', 'args', 'kwargs', '__dict__', '__weakref__'

    def __init__(self, *args, **kwargs):
        if not args:
            raise TypeError('init of vast_fragment needs an argument')
        if len(args) < 2:
            raise TypeError('type "vast_fragment" takes at least one argument')
        self.fn, *self.args = args
        if not callable(self.fn):
            raise TypeError('the first argument must be callable')
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        kwargs.update(self.kwargs)
        return self.fn(*self.args, *args, **kwargs)

    def __reduce__(self):
        return type(self), (self.fn,), (self.fn, self.args, self.kwargs or None, self.__dict__ or None)

    def __setstate__(self, state):
        if not isinstance(state, tuple):
            raise TypeError('argument to __setstate__ must be a tuple')
        if len(state) != 4:
            raise TypeError(f'expected 4 items in state, got {len(state)}')
        self.fn, self.args, self.kwargs, namespace = state
        self.__dict__ = namespace if namespace else {}
            

