import os
import requests

from typing import Callable, List, Tuple

from ..vast import Vast

class VastSession(Vast):
    def __init__(self, workers: int= 16):
        super().__init__(workers=workers)
        self.workers = workers
        self.session = requests.Session()
        rqAdapters = requests.adapters.HTTPAdapter(
            pool_connections = workers, 
            pool_maxsize = workers+4, 
            max_retries = 3
        )
        self.session.mount("https://", rqAdapters)
        self.session.mount('http://', rqAdapters)
        self.session.headers.update({
                "Accept-Encoding": "gzip, deflate",
                "User-Agent" : "gzip,  Python Vast Requests Client"
        })
        self.basepath = os.path.realpath(os.getcwd())
    
    def bulk_requests(self, calls: List[Tuple[Tuple[str, str], dict]], **kwargs: dict):
        return self.run_in_eventloop(self.session.request, calls, **kwargs)