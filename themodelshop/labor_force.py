from collections import deque
from numpy import array as nparray


class LaborPool():
    """

    The labor pool is a data structure that maintains a pool of
    workers. Each of the workers is represented by a minimal set of
    representative numbers. Each item has additional
    statistics such as 'average accuracy', etc...
    """
    def __init__(
        self,
        *statistics,
        maxlen:int=10000
    ):
        self.pool = {statistic: deque(maxlen=maxlen) for statistic in statistics}

    def copy_worker(self,worker):
        # Get 
        raise NotImplementedError

    def seed_pool(self,worker):
        # This adds workers to the pool.
        workers = self.copy_worker(worker)

    