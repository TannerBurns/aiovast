
from ..vast import Vast

class vast_loop(Vast):

    def __init__(self, workers: int= 16):
        super().__init__(workers=workers)
    
    def __call__(self, fn):
        
        def vloop(*args, **kwargs):
            fn(*args, **kwargs)
            return self.run_in_eventloop(*args, **kwargs)
        
        return vloop
    

