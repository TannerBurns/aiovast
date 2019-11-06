import asyncio
import hashlib
import time
import sys

from concurrent.futures import ThreadPoolExecutor
from typing import Callable, List, Tuple, Awaitable, Any, Union, NewType

from tqdm import tqdm
from .utils import EventLoopReport, VastEvent, vast_fragment

class Vast(object):
    Eventloop = NewType(
        'Eventloop', 
        asyncio.windows_events._WindowsSelectorEventLoop
    ) if sys.platform == 'win32' else NewType(
        'Eventloop', 
        asyncio.unix_events._UnixSelectorEventLoop
    )

    def __init__(self, workers: int= 16, loop: Eventloop= None):
        """Vast class
        
        Keyword Arguments:
            workers {int} -- number of asnycio workers (default: {16})
        """
        self.workers = workers
        self.loop = loop
        self.executor = None


    def _execute(self, fn: Callable, args: list= [], kwargs: dict= {}) -> Any:
        return fn(*args, **kwargs)
    

    async def _get_future(self, fn: Callable, args: list= [], kwargs: dict= {}) -> Awaitable:
        return self.loop.run_in_executor(self.executor, vast_fragment(self._execute, fn, args, kwargs))
    

    async def run_in_executor(self, listOfFutures: List[Awaitable]) -> list:
        with ThreadPoolExecutor(max_workers= self.workers) as self.executor:
            return [
                await asyncio.gather(
                    *listOfFutures[index:index+self.workers]
                )
                for index in range(0, len(listOfFutures), self.workers)
            ]


    def run_in_eventloop(
        self, 
        fn: Callable, 
        listOfArgs: List[Tuple[list, dict]], 
        report: bool= False,
        disable_progress_bar: bool= False) -> Union[list, EventLoopReport]:
        if report:
            start_time = time.time()
            results = self.run_in_eventloop(fn, listOfArgs, disable_progress_bar=disable_progress_bar)
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
                len(results),
                hashlib.sha256(
                    str(results).encode()
                ).hexdigest(),
                start_time,
                stop_time,
                stop_time - start_time,
                results
            )
            
        self.loop = self.loop or asyncio.new_event_loop()
        return [
            future.result()
            for index in tqdm(range(0, len(listOfArgs), self.workers), disable= disable_progress_bar)
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
    

    def run_vast_events(self, 
    listOfVastEvents: List[VastEvent], 
    **kwargs: dict) -> Union[List[list], List[EventLoopReport]]:
        return [
            self.run_in_eventloop(vastEvent.fn, vastEvent.listOfArgs, **kwargs)
            for vastEvent in listOfVastEvents
        ]
        