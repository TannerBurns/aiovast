import asyncio

from multiprocessing import Pool
from functools import partial
from typing import Callable, List, Tuple

class Swarmy(object):
    def __init__(self, swarms: int= 4, workers: int= 16):
        """swarmy class
        
        Keyword Arguments:
            swarms {int} -- number of processes (default: {4})
            workers {int} -- number of asnycio workers (default: {16})
        """
        self.swarms = swarms
        self.workers = workers
    
    async def _execute(self, fn: Callable, args: list= [], kwargs: dict= {}):
        if args:
            return fn(*args)
        elif args and kwargs:
            return fn(*args, **kwargs)
        else:
            return fn()
    
    async def async_work(self, fn: Callable, args: list= [], kwargs: dict= {}):
        if args:
            return await self._execute(fn, args)
        elif args and kwargs:
            return await self._execute(fn, args, kwargs)
        else:
            return await self._execute(fn)
    
    async def async_swarm(self, fn: Callable, argumentslist: List[Tuple[list, dict]]):
        results = []
        for index in range(0, len(argumentslist), self.workers):
            for arguments in argumentslist[index:index+self.workers]:
                if len(arguments) == 2:
                    if type(arguments[0]) == list and type(arguments[1]) == dict:
                        results.append(await self.async_work(fn, arguments[0], arguments[1]))
                    elif type(arguments[0]) == dict and type(arguments[1]) == list:
                        results.append(await self.async_work(fn, arguments[1], arguments[0]))
                elif len(arguments) == 1:
                    if type(arguments[0]) == list:
                        results.append(await self.async_work(fn, args = arguments[0]))
                    elif type(arguments[0]) == dict:
                        results.append(await self.async_work(fn, kwargs = arguments[0]))
                else:
                    results.append(await self.async_work(fn))
        return results

    def run_async_swarm(self, fn: Callable, argumentslist: List[Tuple[list, dict]]):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.async_swarm(fn, argumentslist))
    
    def swarm(self, fn: Callable, argumentslist: List[Tuple[list, dict]]):
        groupedargs = [
            argumentslist[index:index+int(len(argumentslist)/self.swarms)]
            for index in range(0, len(argumentslist), int(len(argumentslist)/self.swarms))
        ]
        worker = partial(self.run_async_swarm, fn)
        with Pool(processes=self.swarms) as pool:
            return [res for results in pool.map(worker, groupedargs) for res in results]
    