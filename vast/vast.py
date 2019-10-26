import asyncio

from multiprocessing import Pool
from functools import partial
from typing import Callable, List, Tuple

class Vast(object):
    def __init__(self, max_processes: int= 4, workers: int= 16):
        """swarmy class
        
        Keyword Arguments:
            max_processes {int} -- max number of processes (default: {4})
            workers {int} -- number of asnycio workers (default: {16})
        """
        self.max_processes = max_processes
        self.workers = workers
    
    async def _execute(self, fn: Callable, args: list= [], kwargs: dict= {}):
        if args:
            return fn(*args)
        elif args and kwargs:
            return fn(*args, **kwargs)
        else:
            return fn()
    
    async def execute_in_async(self, fn: Callable, args: list= [], kwargs: dict= {}):
        if args:
            return await self._execute(fn, args)
        elif args and kwargs:
            return await self._execute(fn, args, kwargs)
        else:
            return await self._execute(fn)
    
    async def run_async(self, fn: Callable, argumentslist: List[Tuple[list, dict]]):
        results = []
        for index in range(0, len(argumentslist), self.workers):
            for arguments in argumentslist[index:index+self.workers]:
                if len(arguments) == 2:
                    if type(arguments[0]) == list and type(arguments[1]) == dict:
                        results.append(await self.execute_in_async(fn, arguments[0], arguments[1]))
                    elif type(arguments[0]) == dict and type(arguments[1]) == list:
                        results.append(await self.execute_in_async(fn, arguments[1], arguments[0]))
                elif len(arguments) == 1:
                    if type(arguments[0]) == list:
                        results.append(await self.execute_in_async(fn, args = arguments[0]))
                    elif type(arguments[0]) == dict:
                        results.append(await self.execute_in_async(fn, kwargs = arguments[0]))
                else:
                    results.append(await self.execute_in_async(fn))
        return results

    def run_in_async(self, fn: Callable, argumentslist: List[Tuple[list, dict]]):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.run_async(fn, argumentslist))
    
    def run_in_bulk(self, fn: Callable, argumentslist: List[Tuple[list, dict]]):
        groupedargs = [
            argumentslist[index:index+int(len(argumentslist)/self.max_processes)]
            for index in range(0, len(argumentslist), int(len(argumentslist)/self.max_processes))
        ]
        worker = partial(self.run_in_async, fn)
        with Pool(processes=self.max_processes) as pool:
            return [res for results in pool.map(worker, groupedargs) for res in results]
    