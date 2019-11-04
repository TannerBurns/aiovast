# Vast

    Python3 library to easily scale using asyncio

# Usage

    Python3.6+

# Methods

    Vast

        run_in_eventloop(fn, listOfArgs, report=False, disable_progress_bar=False)
            run function in eventloop, if report equals true return EventLoopReport
                EventLoopReport:
                function_name       str
                function_docstring  str
                function_hash       str
                function_sha256     str
                input_count         int
                input_sha256        str
                start_time          int
                stop_time           int
                runtime             int
                results             list
        
        run_vast_events(listOfVastEvents, report=False, disable_progress_bar=False)
            run a vast event
                VastEvent:
                fn                  Callable
                listOfArgs          List[Tuple[list, dict]]


    Vast Requests

        bulk_requests(listOfCalls) - run all requests calls in an eventloop
            calls = [(method, url, listOfKwargs), ...]
        
        bulk_get(url, listOfKwargs) - run all requests for url on given kwargs in listOfKwargs

        bulk_post(url, listOfKwargs) - run all requests for url on given kwargs in listOfKwargs

        bulk_put(url, listOfKwargs) - run all requests for url on given kwargs in listOfKwargs

        bulk_delete(url, listOfKwargs) - run all requests for url on given kwargs in listOfKwargs
        
        bulk_head(url, listOfKwargs) - run all requests for url on given kwargs in listOfKwargs
        

# Examples

Example using class
```python
import time

from vast import Vast

def add(x, y): return x + y

if __name__ == '__main__':
    vast = Vast(workers=16)

    args = [[[x, y]] for x in range(0, 200) for y in range(200, 400)]
    start = time.time()
    rets = vast.run_in_eventloop(add, args)
    print(f'Completed in: {time.time() - start}')
```

Example using decorator
```python
from vast.decorators import vast_loop

def add(x, y): return x + y

@vast_loop(workers=16)
def run_in_bulk(fn, listOfArgs, report=False, disable_progress_bar=False):
    print(f'running {fn.__name__}')

if __name__ == '__main__':
    args = [[[x, y]] for x in range(0, 5) for y in range(5, 10)]
    rets = run_in_bulk(add, args)
```

Vast session for sending bulk requests
```python
from vast.requests import VastSession

session = VastSession(workers=4)
calls = [
    ('get', 'https://www.google.com', [{'headers': {'AcceptEncoding''application/json'}}]), ('post', 'https://www.github.com')]
responses = session.bulk_requests(calls)
```

