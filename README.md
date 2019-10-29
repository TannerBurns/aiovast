# Vast

    Python3 library to easily scale using asyncio

# Usage

    Python3.6+

# Methods

    Vast

        run_in_eventloop(fn, listOfArgs) - run function using asyncio in an eventloop and get results for all calls
    

    Vast Requests

        bulk_requests(listOfCalls) - run all requests calls in an eventloop
            calls = [(method, url, listOfKwargs), ...]
        
        bulk_get(url, listOfKwargs) - run all requests for url on given kwargs in listOfKwargs
        bulk_post(url, listOfKwargs) - run all requests for url on given kwargs in listOfKwargs
        bulk_put(url, listOfKwargs) - run all requests for url on given kwargs in listOfKwargs
        bulk_delete(url, listOfKwargs) - run all requests for url on given kwargs in listOfKwargs
        bulk_head(url, listOfKwargs) - run all requests for url on given kwargs in listOfKwargs
        

# Examples

```python
import time

from vast import Vast

def add(x, y): return x + y

if __name__ == '__main__':
    vast = Vast(workers=16)

    args = [([x, y], ) for x in range(0, 200) for y in range(200, 400)]
    start = time.time()
    rets = vast.run_in_eventloop(add, args)
    print(f'Completed in: {time.time() - start}')

```

```python
from vast.requests import VastSession

session = VastSession(workers=4)
calls = [
    ('get', 'https://www.google.com', [{'headers': {'AcceptEncoding''application/json'}}]), ('post', 'https://www.github.com')]
responses = session.bulk_requests(calls)
```

