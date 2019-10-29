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

    def bulk_get(self, url, listOfKwargs: List[dict]= [{}]):
        return self.run_in_eventloop(self.session.get, [([url], kw) for kw in listOfKwargs])
    
    def bulk_post(self, url, listOfKwargs: List[dict]= [{}]):
        return self.run_in_eventloop(self.session.post, [([url], kw) for kw in listOfKwargs])
    
    def bulk_put(self, url, listOfKwargs: List[dict]= [{}]):
        return self.run_in_eventloop(self.session.put, [([url], kw) for kw in listOfKwargs])
    
    def bulk_delete(self, url, listOfKwargs: List[dict]= [{}]):
        return self.run_in_eventloop(self.session.delete, [([url], kw) for kw in listOfKwargs])
    
    def bulk_head(self, url, listOfKwargs: List[dict]= [{}]):
        return self.run_in_eventloop(self.session.head, [([url], kw) for kw in listOfKwargs])
    
    def bulk_requests(self, calls: List[Tuple[str, str, List[dict]]]):
        bulk_get = [call[1:] for call in calls if call[0].lower() == 'get']
        bulk_post = [call[1:] for call in calls if call[0].lower() == 'post']
        bulk_put = [call[1:] for call in calls if call[0].lower() == 'put']
        bulk_delete = [call[1:] for call in calls if call[0].lower() == 'delete']
        bulk_head = [call[1:] for call in calls if call[0].lower() == 'head']
        responses = []
        if bulk_get:
            responses.extend([self.bulk_get(*call) for call in bulk_get])
        if bulk_post:
            responses.extend([self.bulk_post(*call) for call in bulk_post])
        if bulk_put:
            responses.extend([self.bulk_put(*call) for call in bulk_put])
        if bulk_delete:
            responses.extend([self.bulk_delete(*call) for call in bulk_delete])
        if bulk_head:
            responses.extend([self.bulk_head(*call) for call in bulk_head])
        return responses

