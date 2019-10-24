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

from swarmy import Swarmy

def add(x, y):
    return x + y

if __name__ == "__main__":
    args = [([x, y], ) for x in range(0, 300) for y in range(300, 600)]
    swarmy = Swarmy(swarms=4, workers=16)

    # multiprocess pool + asyncio
    # slower for most task
    start = time.time()
    rets = swarmy.swarm(add, args)
    stop = time.time() - start
    print("Completed swarm in: {0}".format(stop))

    # asyncio
    start = time.time()
    rets = swarmy.run_async_swarm(add, args)
    stop = time.time() - start
    print("Completed async swarm in: {0}".format(stop))

    # asyncio in Ipython foreground loop
    start = time.time()
    rets = await swarmy.async_swarm(add, args)
    stop = time.time() - start
    print("Completed async swarm in: {0}".format(stop))
```

