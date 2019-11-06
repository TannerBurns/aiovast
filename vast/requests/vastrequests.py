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
    
    def bulk_get_requests(self, calls: List[Tuple[Tuple[str], dict]], **kwargs: dict):
        return self.run_in_eventloop(self.session.get, calls, **kwargs)
    
    def bulk_post_requests(self, calls: List[Tuple[Tuple[str], dict]], **kwargs: dict):
        return self.run_in_eventloop(self.session.post, calls, **kwargs)
    
    def bulk_put_requests(self, calls: List[Tuple[Tuple[str], dict]], **kwargs: dict):
        return self.run_in_eventloop(self.session.put, calls, **kwargs)
    
    def bulk_delete_requests(self, calls: List[Tuple[Tuple[str], dict]], **kwargs: dict):
        return self.run_in_eventloop(self.session.delete, calls, **kwargs)
    
    def bulk_head_requests(self, calls: List[Tuple[Tuple[str], dict]], **kwargs: dict):
        return self.run_in_eventloop(self.session.head, calls, **kwargs)
    
    def bulk_requests(self, calls: List[Tuple[Tuple[str, str], dict]], **kwargs: dict):
        return self.run_in_eventloop(self.session.request, calls, **kwargs)