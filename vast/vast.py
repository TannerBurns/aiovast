import asyncio

from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import Callable, List, Tuple

class Vast(object):
    def __init__(self, workers: int= 16):
        """Vase class
        
        Keyword Arguments:
            workers {int} -- number of asnycio workers (default: {16})
        """
        self.workers = workers

    def _execute(self, fn: Callable, args: list= [], kwargs: dict= {}):
        if args:
            return fn(*args)
        elif kwargs:
            return fn(**args)
        elif args and kwargs:
            return fn(*args, **kwargs)
        else:
            return fn()
    
    async def _get_future(self, fn: Callable, args: list= [], kwargs: dict= {}):
        return self.loop.run_in_executor(self.executor, partial(self._execute, fn, args, kwargs))
    
    async def _run_in_executor(self, fn: Callable, listOfArgs: List[Tuple[list, dict]]):
        with ThreadPoolExecutor(max_workers= self.workers) as self.executor:
            return [
                await asyncio.gather(
                    *[self._get_future(fn, *args) for args in listOfArgs[index:index+self.workers]]
                )
                for index in range(0, len(listOfArgs), self.workers)
            ]
    
    def run_in_eventloop(self, fn: Callable, listOfArgs: List[Tuple[list, dict]]= list((list, dict))):
        self.loop = asyncio.get_event_loop()
        return [future.result() for future_results in self.loop.run_until_complete(self._run_in_executor(fn, listOfArgs)) for future in future_results]

    
    