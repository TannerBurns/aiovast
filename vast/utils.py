from typing import NamedTuple, List, Tuple, Callable

class EventLoopReport(NamedTuple):
    function_name: str
    function_docstring: str
    function_hash: str
    function_sha256: str
    input_count: int
    input_sha256: str
    start_time: int
    stop_time: int
    runtime: int
    results: list

class VastEvent(NamedTuple):
    fn: Callable
    listOfArgs: List[Tuple[list, dict]]