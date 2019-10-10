import asyncio

from concurrent.futures import ThreadPoolExecutor
from functools import partial
from multiprocessing import Pool
from typing import Callable

class Swarmy:
    def __init__(self, swarms: int= 4, workers: int= 16):
        """swarmy class
        
        Keyword Arguments:
            swarms {int} -- number of processes (default: {4})
            workers {int} -- number of asnycio workers (default: {16})
        """
        self.num_swarms = swarms
        self.num_workers = workers
    
    async def _army(self, fn: Callable, args: list) -> list:
        """_army - complete the work
        
        Arguments:
            fn {Callable} -- function call to map
            group {list} -- sub group that will be mapped to the function
        
        Returns:
            list -- group of returns from the mapped function
        """
        with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            futures = [self.loop.run_in_executor(executor, partial(fn, a)) for a in args if a]
            await asyncio.gather(*futures)
            return [f.result() for f in futures]


    def _swarm_helper(self, fn, args):
        self.loop = asyncio.get_event_loop() or asyncio.new_event_loop()
        return [
            res 
            for i in range(0, len(args), self.num_workers) 
            for res in self.loop.run_until_complete(self._army(fn, args[i:i+self.num_workers]))
        ]
    
    def swarm(self, fn: Callable, args: list) -> list:
        """swarm - process the work for a given fn with multiprocess and asyncio
        
        Arguments:
            fn {Callable} -- function to map
            fullgroup {list} -- full list to map with function
        
        Returns:
            list -- group of results from the mapped pool
        """

        chunked = [
            args[ind:ind+int(len(args)/self.num_swarms)]
            for ind in range(0, len(args), int(len(args)/self.num_swarms))
        ]
        worker = partial(self._swarm_helper, fn)
        with Pool(processes=self.num_swarms) as pool:
            return [r for res in pool.map(worker, chunked) for r in res if r]
    
    def multiprocess_swarm(self, fn: Callable, args: list, chunk_size: int=16) -> list:
        """multiprocess_swarm - swarm only using multiprocess pool
        
        Arguments:
            fn {Callable} -- function to map
            fullgroup {list} -- full list to map with function
            chunk_size {int} -- size for chunking work
        
        Returns:
            list -- group of results from the mapped pool
        """
        chunked = [
            args[ind:ind+chunk_size] 
            for ind in range(0, len(args), chunk_size)
        ]
        with Pool(processes=self.num_swarms) as pool:
            return [
                res
                for ind in range(0, len(chunked), self.num_swarms)
                for res in pool.map(fn, chunked[ind:ind+self.num_swarms])
                if res
            ]
    
    def async_swarm(self, fn: Callable, args: list) -> list:
        """async_swarm - swarm only using asyncio
        
        Arguments:
            fn {Callable} -- function to run async
            args {list} -- arguments to map with function
        
        Returns:
            list -- generator to a list
        """
        self.loop = asyncio.get_event_loop() or asyncio.new_event_loop()
        for ind in range(0, len(args), self.num_workers):
            yield self.loop.run_until_complete(self._army(fn, args[ind:ind+self.num_workers]))
        



