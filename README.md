# Vast

    Python3 library to easily scale up and out using multiprocessing and asyncio

# Usage

    Python3.6+

# Methods

    run_in_bulk(fn, arguments) - scale using a multiprocessing pool and asyncio
    run_in_async(fn, arguments) - scale using just asyncio
    run_async(fn, arguments) - coroutine used in run_in_async

# Example

```python
import time

from vast import Vast

def add(x, y):
    return x + y

if __name__ == "__main__":
    args = [([x, y], ) for x in range(0, 300) for y in range(300, 600)]
    vast = Vast(max_processes=4, workers=16)

    # multiprocess pool + asyncio
    # slower for most task
    start = time.time()
    rets = vast.run_in_bulk(add, args)
    stop = time.time() - start
    print("Completed in: {0}".format(stop))

    # asyncio
    start = time.time()
    rets = vast.run_in_async(add, args)
    stop = time.time() - start
    print("Completed in: {0}".format(stop))

    # asyncio in Ipython foreground loop
    start = time.time()
    rets = await vast.run_async(add, args)
    stop = time.time() - start
    print("Completed in: {0}".format(stop))
```

