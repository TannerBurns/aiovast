from .. import Vast


class vast_loop(Vast):

    def __init__(self, workers: int = 16):
        super().__init__(workers=workers)
    
    def __call__(self, fn):
        
        def vloop(listofArgs: list, **kwargs):
            return self.run_in_eventloop(fn, listofArgs, **kwargs)
        
        return vloop
