from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

class Summary(object):
    """Cache Simulator output"""

    def __init__(self):
        self.total_cache_accesses = 0
        self.num_cache_reads = 0
        self.num_cache_writes = 0
        self.num_invalidates = 0
        self.num_cache_hits = 0
        self.num_cache_misses = 0
        self.hit_ratio = 0
        self.miss_ratio = 0
        self.num_evictions = 0
        self.num_writebacks = 0

    def print_output(self):
        if self.total_cache_accesses != 0:
            self.miss_ratio = self.num_cache_misses / self.total_cache_accesses
            self.hit_ratio = self.num_cache_hits / self.total_cache_accesses

        print("Total number of cache accesses: {}".format(self.total_cache_accesses))
        print("Number of cache reads: {}".format(self.num_cache_reads))
        print("Number of cache writes: {}".format(self.num_cache_writes))
        print("Number of invalidates: {}".format(self.num_invalidates))
        print("Number of cache hits: {}".format(self.num_cache_hits))
        print("Number of cache misses: {}".format(self.num_cache_misses))
        print("Cache hit ratio: {}".format(self.hit_ratio))
        print("Cache miss ratio: {}".format(self.miss_ratio))
        print("Number of evictions: {}".format(self.num_evictions))
        print("Number of writebacks: {}".format(self.num_writebacks))
