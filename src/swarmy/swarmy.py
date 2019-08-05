import asyncio
import concurrent.futures

from functools import partial
from multiprocessing import Pool
from typing import Callable, Tuple

class swarmy:
    def __init__(self, swarms=4, workers=16):
        """swarmy class
        
        Keyword Arguments:
            swarms {int} -- number of processes (default: {4})
            workers {int} -- number of asnycio workers (default: {16})
        """
        self.num_swarms = swarms
        self.num_workers = workers
    
    async def _soldiers(self, fn: Callable, group: list) -> list:
        """_soldiers - complete the work
        
        Arguments:
            fn {Callable} -- function call to map
            group {list} -- sub group that will be mapped to the function
        
        Returns:
            list -- group of returns from the mapped function
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            loop = asyncio.get_event_loop()
            futures = [
                loop.run_in_executor(executor, partial(fn, item)) 
                for item in group if item
            ]
        await asyncio.gather(*futures)
        return [f.result() for f in futures]

    def _army(self, fn: Callable, args: list) -> list:
        """_army - assemble the work
        
        Arguments:
            fn {Callable} -- function to map
            fullgroup {list} -- full list to map with function
        
        Returns:
            list -- group of returns from the mapped function
        """
        loop = asyncio.get_event_loop()
        return [
            res 
            for ind in range(0, len(args), self.num_workers) 
            for res in loop.run_until_complete(
                self._soldiers(fn, args[ind:ind+self.num_workers])
            )
            if res
        ]
    
    def swarm(self, fn: Callable, args: list) -> list:
        """swarm - process the work for a given fn
        
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
        worker = partial(self._army, fn)
        with Pool(processes=self.num_swarms) as pool:
            return [
                res
                for rets in pool.map(worker, chunked)
                for res in rets
                if res 
            ]
    
    def na_swarm(self, fn: Callable, args: list, chunk_size: int=16) -> list:
        """na_swarm - non asyncio swarm army process the work
        
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
        



