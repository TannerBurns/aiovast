# Vast

<!--Badges-->
![MIT badge](https://img.shields.io/badge/license-MIT-black)
![Version badge](https://img.shields.io/github/manifest-json/v/tannerburns/vast?color=red)
![RepoSize badge](https://img.shields.io/github/repo-size/tannerburns/vast?color=green)
![Python3.6 badge](https://img.shields.io/badge/python-v3.6+-blue?logo=python&logoColor=yellow)
![Platform badge](https://img.shields.io/badge/platform-linux%20%7C%20osx%20%7C%20win32-yellow)

    A utility to easily scale functionality


## Table of Contents

- [ Requirements ](#requirements)
- [ Installation ](#install)
- [ Information ](#information)
    - [ Vast ](#vast)
        - [ Vast Event Loop ](#vasteventloop)
    - [ VastSession ](#vastsession)
        - [ Vast Bulk Requests ](#vastbulkrequests)
            - [ Vast Bulk Get ](#vastbulkget)
            - [ Vast Bulk Post ](#vastbulkpost)
            - [ Vast Bulk Put ](#vastbulkput)
            - [ Vast Bulk Delete ](#vastbulkdelete)
            - [ Vast Bulk Head ](#vastbulkhead)
- [ Examples ](#examples)

<br>

<a name="requirements"></a>
## Requirements
* Python3.6+

<br>

<a name="install"></a>
## Installation
* Create a new virtual environment with python 3.6+

    * Install the vast library
    ```bash
    $ git clone https://www.github.com/tannerburns/vast
    $ cd vast
    $ pip3 install .
    ```

<br>

<a name="information"></a>
## Information
    Details about the vast utility


<a name="#vast"></a>
### Vast

    Main variables

* loop: asyncio.new_event_loop
* max_async_pool: int, default=32
* max_futures_pool: int, default=10000

<br>

<a name="#vasteventloop"></a>
#### Vast Event Loop

    Main method

* run_in_eventloop
    * arg1: functionObject, Callable
        * the function to run in the event loop
    * arg2: listOfArgs, list
        * the list of arguments to be mapped to the function in the event loop
    * kwarg: report, default= False
        * returns results and statistics about the event loop runtime
    * kwarg: disable_progress_bar, default= False
        * disables the progress bar from printing while the event loop runs
    * kwarg: progress_bar_color, default= green
        * provide another color for the progress bar template

<br>

<a name="#vastsession"></a>
### VastSession

    Variables

* loop: asyncio.new_event_loop
* max_async_pool: int, default=32
* max_futures_pool: int, default=10000
* self.session: requests.session

<br>

<a name="#vastbulkrequests"></a>
#### Vast Bulk Requests

    A function that can handle any method requests will accept     

* bulk_requests
    * arg1: listOfCalls, list
        * format: [ [[method: string, url: string], options: dictionary], [[method: string, url: string], options: dictionary], .. ]

<br>

```
Function calls for single method types
```
<a name="#vastbulkget"></a>
##### Vast Bulk Get
* bulk_get_requests
    * arg1: listOfCalls, list
        * format: [ [[url: string], options: dictionary], [[url: string], options: dictionary], .. ]

<a name="#vastbulkpost"></a>
##### Vast Bulk Post
* bulk_post_requests
    * arg1: listOfCalls, list
        * format: [ [[url: string], options: dictionary], [[url: string], options: dictionary], .. ]

<a name="#vastbulkput"></a>
##### Vast Bulk Put
* bulk_put_requests
    * arg1: listOfCalls, list
        * format: [ [[url: string], options: dictionary], [[url: string], options: dictionary], .. ]

<a name="#vastbulkdelete"></a>
##### Vast Bulk Delete
* bulk_delete_requests
    * arg1: listOfCalls, list
        * format: [ [[url: string], options: dictionary], [[url: string], options: dictionary], .. ]

<a name="#vastbulkhead"></a>
##### Vast Bulk Head
* bulk_head_requests
    * arg1: listOfCalls, list
        * format: [ [[url: string], options: dictionary], [[url: string], options: dictionary], .. ]

<br>

<a name="#examples"></a>
## Examples
```python
#Basic add example
def add(x, y): return x + y

if __name__ == '__main__':
    rets = [add(x, y) for x in range(0, 5) for y in range(5, 10)]
```

```python
#Example bulk add using vast class
from vast import Vast

def add(x, y): return x + y

if __name__ == '__main__':
    vast = Vast()
    args = [[[x, y]] for x in range(0, 5) for y in range(5, 10)]
    rets = vast.run_in_eventloop(add, args)
```

```python
#Example using Vast context manager
from vast import Vast

def add(x, y): return x + y

if __name__ == '__main__':
    args = [[[x, y]] for x in range(0, 5) for y in range(5, 10)]
    with Vast() as vast:
        rets = vast.run_in_eventloop(add, args)
```

```python
#Example bulk add using decorator
from vast.decorators import vast_loop

@vast_loop(max_async_pool=16)
def add_in_bulk(x, y):
    return x+y

if __name__ == '__main__':
    args = [[[x, y]] for x in range(0, 5) for y in range(5, 10)]
    rets = add_in_bulk(args)
```

```python
#Vast session for sending bulk requests
from vast.requests import VastSession

session = VastSession(max_async_pool=4)
calls = [
    (['get', 'https://www.google.com'], {'headers': {'User-Agent':'custom'}}),
    (['post', 'https://www.github.com'], )
]
responses = session.bulk_requests(calls)
```
