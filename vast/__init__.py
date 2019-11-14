import asyncio
import hashlib
import time
import sys

from concurrent.futures import ThreadPoolExecutor
from typing import Callable, List, Awaitable, Any, Union, NewType

from colored import fg
from tqdm import tqdm
from .utils import EventLoopReport, VastEvent, vast_fragment

class Vast(object):
    """simple utilities to convert a synchronous task into a asynchronous task
    """

    Eventloop = NewType('Eventloop', asyncio.windows_events._WindowsSelectorEventLoop) \
        if sys.platform == 'win32' else NewType('Eventloop', asyncio.unix_events._UnixSelectorEventLoop)

    def __init__(self, loop: Eventloop= None, max_async_pool: int= 32, max_futures_pool: int= 1000):
        self.loop = loop or asyncio.new_event_loop()
        self.max_futures_pool = max_futures_pool
        self.max_async_pool = max_async_pool
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.loop = None
        if hasattr(self, 'executor'):
            self.executor = None

    def _futures_execute(self, fn: Callable, args: list= [], kwargs: dict= {}) -> Any:
        return fn(*args, **kwargs)
    
    async def create_futures(self, fn: Callable, args: list= [], kwargs: dict= {}) -> Awaitable:
        return self.loop.run_in_executor(self.executor, vast_fragment(self._futures_execute, fn, args, kwargs))
    
    async def run_executor(self, listOfFutures: List[Awaitable]) -> list:
        with ThreadPoolExecutor(max_workers= self.max_async_pool) as self.executor:
            return [
                await asyncio.gather(
                    *listOfFutures[index:index+self.max_async_pool]
                )
                for index in range(0, len(listOfFutures), self.max_async_pool)
            ]

    def run_in_eventloop(
        self, 
        fn: Callable, 
        listOfArgs: List[Union[list, dict]],
        report: bool= False,
        disable_progress_bar: bool= False,
        progress_bar_color: str= 'green_3a') -> Union[list, EventLoopReport]:
        if report:
            start_time = time.time()
            # recursive call to run_in_eventloop without report == True
            results = self.run_in_eventloop(
                fn, 
                listOfArgs, 
                disable_progress_bar=disable_progress_bar, 
                progress_bar_color=progress_bar_color
            )
            stop_time = time.time()
            # return a single EventLoopReport (NamedTuple) object which contains the results of all assigned work
            return EventLoopReport(
                str(fn.__name__), str(fn.__doc__), str(fn.__hash__()),
                hashlib.sha256(
                    str(fn.__name__).encode() + str(fn.__doc__).encode() + str(fn.__hash__()).encode()
                ).hexdigest(), 
                len(listOfArgs), hashlib.sha256(str(listOfArgs).encode()).hexdigest(),
                len(results), hashlib.sha256(str(results).encode()).hexdigest(),
                start_time, stop_time, stop_time - start_time, results
            )

        # return all the assigned work, list of results for each arg in listOfArgs    
        return [
            future.result()
            for index in tqdm(
                range(0, len(listOfArgs), self.max_futures_pool), 
                disable= disable_progress_bar,
                bar_format=(
                    '%s{l_bar}{bar}| {n_fmt}/{total_fmt} Chunks [{elapsed}<{remaining},' \
                    ' {rate_fmt}{postfix}]' % fg(progress_bar_color)
                )
            )
            for future_results in self.loop.run_until_complete(
                self.run_executor(
                    [self.create_futures(fn, *args) for args in listOfArgs[index:index+self.max_futures_pool]]
                )
            )
            for future in future_results        
        ]
    
    def run_vast_events(self, 
    listOfVastEvents: List[VastEvent], 
    **kwargs: dict) -> Union[List[list], List[EventLoopReport]]:
        # return all assigned work for list of vast events (a fn and list of arguments)
        # ? Could this become a multiprocess pool, and split up the vast events into a mutliproc pool
        return [
            self.run_in_eventloop(vastEvent.fn, vastEvent.listOfArgs, **kwargs)
            for vastEvent in listOfVastEvents
        ]
        