# Swarm Army

    Python3 library to easily scale up and out using multiprocessing and asyncio

# Usage

    Python3.6+

# Methods

    swarm(fn, arguments) - scale using a multiprocessing pool and asyncio
    multiprocess_swarm(fn, arguments, chunk_size=16) - scale using just a mutliprocessing pool
    async_swarm(fn, arguments) - scale using just asyncio

# Example

    ```python
    import time

    from swarmy import swarmy

    def add(args):
        '''
        :param args:
        :return sum of args:
        '''
        return args[0]+args[1]

    if __name__ == "__main__":
        args = [(x, y) for x in range(0, 300) for y in range(300, 600)]
        swarmy = swarmy()
        start = time.time()
        rets = swarmy.swarm(add, args)
        stop = time.time() - start

        print(len(rets))
        print("Completed in: {0}".format(stop))
    ```