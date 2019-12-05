import asyncio
import hashlib
import time
import sys

from concurrent.futures import ThreadPoolExecutor
from typing import Callable, List, Awaitable, Any, Union, NewType

from colored import fg, style
from tqdm import tqdm
from .utils import EventLoopReport, VastEvent, vast_fragment

class Vast(object):
    """simple utilities to convert a synchronous task into a asynchronous task
    """

    Eventloop = NewType('Eventloop', asyncio.windows_events._WindowsSelectorEventLoop) \
        if sys.platform == 'win32' else NewType('Eventloop', asyncio.unix_events._UnixSelectorEventLoop)

    def __init__(self, loop: Eventloop= None, max_async_pool: int= 32, max_futures_pool: int= 10000):
        self.loop = loop or asyncio.new_event_loop()
        self.max_futures_pool = max_futures_pool
        self.max_async_pool = max_async_pool
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.loop = None

    def _futures_execute(self, fn: Callable, args: list= [], kwargs: dict= {}) -> Any:
        return fn(*args, **kwargs)
    
    async def run_executor(
        self,
        fn,
        listOfArgs: list,
        disable_progress_bar: bool,
        progress_bar_color: str) -> list:
        bar_format = '%s{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining},' \
                    ' {rate_fmt}{postfix}]' % fg(progress_bar_color)
        with ThreadPoolExecutor(max_workers= self.max_async_pool) as executor:
            listOfFutures = [
                self.loop.run_in_executor(executor, vast_fragment(self._futures_execute, fn, *args))
                for args in listOfArgs
            ]
            return [
                await result
                for result in tqdm(
                    asyncio.as_completed(listOfFutures), 
                    total=len(listOfFutures),
                    disable= disable_progress_bar,
                    bar_format=bar_format
                )
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
        # if bar is not disabled; print newline for progress bar padding 
        if not disable_progress_bar:
            print()
        # get event loop results  
        event_loop_results = [
            future_result
            for index in range(0, len(listOfArgs), self.max_futures_pool)
            for future_result in self.loop.run_until_complete(
                self.run_executor(
                    fn,
                    listOfArgs[index:index+self.max_futures_pool],
                    disable_progress_bar,
                    progress_bar_color
                )
            )        
        ]
        # if bar is not disabled; reset style after progress bar print
        if not disable_progress_bar:
            print(style.RESET)
        # return the event loop results
        return event_loop_results

    
    def run_vast_events(self, 
    listOfVastEvents: List[VastEvent], 
    **kwargs: dict) -> Union[List[list], List[EventLoopReport]]:
        # return all assigned work for list of vast events (a fn and list of arguments)
        # ? Could this become a multiprocess pool, and split up the vast events into a mutliproc pool
        return [
            self.run_in_eventloop(vastEvent.fn, vastEvent.listOfArgs, **kwargs)
            for vastEvent in listOfVastEvents
        ]
        