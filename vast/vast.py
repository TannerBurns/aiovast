import asyncio
import hashlib
import time

from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import Callable, List, Tuple, Awaitable, Any

from .utils import EventLoopReport

class Vast(object):
    def __init__(self, workers: int= 16):
        """Vase class
        
        Keyword Arguments:
            workers {int} -- number of asnycio workers (default: {16})
        """
        self.workers = workers

    def _execute(self, fn: Callable, args: list= [], kwargs: dict= {}) -> Any:
        if args and not kwargs:
            return fn(*args)
        elif kwargs and not args:
            return fn(**kwargs)
        elif args and kwargs:
            return fn(*args, **kwargs)
        else:
            return fn()
    
    async def _get_future(self, fn: Callable, args: list= [], kwargs: dict= {}) -> Awaitable:
        return self.loop.run_in_executor(self.executor, partial(self._execute, fn, args, kwargs))
    
    async def run_in_executor(self, listOfFutures: List[Awaitable]) -> list:
        with ThreadPoolExecutor(max_workers= self.workers) as self.executor:
            return [
                await asyncio.gather(
                    *listOfFutures[index:index+self.workers]
                )
                for index in range(0, len(listOfFutures), self.workers)
            ]

    def run_in_eventloop(self, fn: Callable, listOfArgs: List[Tuple[list, dict]]= list((list, dict))) -> list:
        self.loop = asyncio.new_event_loop()
        return [
            future.result()
            for index in range(0, len(listOfArgs), self.workers)
            for args in listOfArgs[index:index+self.workers]
            for future_results in self.loop.run_until_complete(
                self.run_in_executor(
                    [
                        self._get_future(fn, *args)
                    ]
                )
            )
            for future in future_results
        ]
    
    def run_el_and_report(self, fn: Callable, listOfArgs: List[Tuple[list, dict]]= list((list, dict))) -> EventLoopReport:
        start_time = time.time()
        results = self.run_in_eventloop(fn, listOfArgs)
        stop_time = time.time()
        return EventLoopReport(
            str(fn.__name__),
            str(fn.__doc__),
            str(fn.__hash__()),
            hashlib.sha256(
                str(fn.__name__).encode() + str(fn.__doc__).encode() + str(fn.__hash__()).encode()
            ).hexdigest(),
            len(listOfArgs),
            hashlib.sha256(
                str(listOfArgs).encode()
            ).hexdigest(),
            start_time,
            stop_time,
            stop_time - start_time,
            results
        )
