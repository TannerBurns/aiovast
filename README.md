# Vast

![MIT badge](https://img.shields.io/badge/license-MIT-black)
![Version badge](https://img.shields.io/github/manifest-json/v/tannerburns/vast?color=red)
![RepoSize badge](https://img.shields.io/github/repo-size/tannerburns/vast?color=green)
![Python3.6 badge](https://img.shields.io/badge/python-v3.6+-blue?logo=python&logoColor=yellow)
![Platform badge](https://img.shields.io/badge/platform-linux%20%7C%20osx%20%7C%20win32-yellow)


    Python3 library to easily scale using asyncio

# Usage

    Python3.6+

# Methods

    Vast

        run_in_eventloop(fn, listOfArgs, report=False, disable_progress_bar=False, progress_bar_color='green_3a')
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


    Vast Requests - VastSession

        bulk_requests(listOfCalls) - run all requests calls in an eventloop
            calls = [([method, url], kwargs), ...]
        
        bulk_get(listOfCalls) - run all requests
        bulk_post(listOfCalls) - run all requests
        bulk_put(listOfCalls) - run all requests
        bulk_delete(listOfCalls) - run all requests
        bulk_head(listOfCalls) - run all requests
            calls = [([url], kwargs), ...]
        

# Basic Examples

Basic add example
```python
def add(x, y): return x + y

if __name__ == '__main__':
    rets = [add(x, y) for x in range(0, 5) for y in range(5, 10)]
```

Example bulk add using vast class
```python
from vast import Vast

def add(x, y): return x + y

if __name__ == '__main__':
    vast = Vast(workers=16)

    args = [[[x, y]] for x in range(0, 5) for y in range(5, 10)]
    rets = vast.run_in_eventloop(add, args)
```

Example bulk add using decorator
```python
from vast.decorators import vast_loop

@vast_loop(workers=16)
def add_in_bulk(x, y):
    return x+y

if __name__ == '__main__':
    args = [[[x, y]] for x in range(0, 5) for y in range(5, 10)]
    rets = add_in_bulk(args)
```

# Bulk Requests Example

Vast session for sending bulk requests
```python
from vast.requests import VastSession

session = VastSession(workers=4)
calls = [
    (['get', 'https://www.google.com'], {'headers': {'User-Agent':'custom'}}),
    (['post', 'https://www.github.com'], )
]
responses = session.bulk_requests(calls)
```

