from typing import NamedTuple

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

