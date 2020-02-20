import requests

from typing import List, Tuple

from .. import Vast


class VastSession(Vast):
    def __init__(self, session: requests.Session = None, raise_exception: bool = True, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.raise_exception = raise_exception
        if session:
            self.session = session
        else:
            self.session = requests.Session()
            rqAdapters = requests.adapters.HTTPAdapter(
                pool_connections=self.max_async_pool,
                pool_maxsize=self.max_async_pool,
                max_retries=3
            )
            self.session.mount("https://", rqAdapters)
            self.session.mount('http://', rqAdapters)
            self.session.headers.update({
                    "Accept-Encoding": "gzip, deflate",
                    "User-Agent": "gzip,  Python Vast Requests Client"
            })

    def refresh_token(self):
        """Use this to add to verify auth is still valid or refresh if out of date.

        :return:
        """
        pass

    def _make_request(self, request_call, url, request_kwargs={}) -> requests.Response:
        """Makes an http request, suppress errors and include content.

        :param session_call: URL the POST request will be made.
        :return: Response
        """
        try:
            response = request_call(url, **request_kwargs)
            if response.status_code == 401:  # Fingers crossed the API has proper status codes
                self.refresh_token()
            return response

        except Exception as e:
            if self.raise_exception:
                raise
            else:
                response = requests.Response()
                response.url = url
                response._content = str(e).encode('utf-8')
                return response

    def get_request(self, url, request_kwargs={}):
        return self._make_request(self.session.get, url, request_kwargs)

    def post_request(self, url, request_kwargs={}):
        return self._make_request(self.session.post, url, request_kwargs)

    def put_request(self, url, request_kwargs={}):
        return self._make_request(self.session.put, url, request_kwargs)

    def head_request(self, url, request_kwargs={}):
        return self._make_request(self.session.head, url, request_kwargs)

    def delete_request(self, url, request_kwargs={}):
        return self._make_request(self.session.delete, url, request_kwargs)

    def bulk_get_requests(self, calls: List[Tuple[Tuple[str], dict]], **kwargs: dict):
        return self.run_in_eventloop(self.get_request, calls, **kwargs)
    
    def bulk_post_requests(self, calls: List[Tuple[Tuple[str], dict]], **kwargs: dict):
        return self.run_in_eventloop(self.post_request, calls, **kwargs)
    
    def bulk_put_requests(self, calls: List[Tuple[Tuple[str], dict]], **kwargs: dict):
        return self.run_in_eventloop(self.put_request, calls, **kwargs)
    
    def bulk_delete_requests(self, calls: List[Tuple[Tuple[str], dict]], **kwargs: dict):
        return self.run_in_eventloop(self.delete_request, calls, **kwargs)
    
    def bulk_head_requests(self, calls: List[Tuple[Tuple[str], dict]], **kwargs: dict):
        return self.run_in_eventloop(self._make_request, [self.session.head, calls], **kwargs)
