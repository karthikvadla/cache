from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

class Output(object):
    """Cache Simulator output"""

    def __init__(self, total_cache_accesses, num_cache_reads,
                 num_cache_writes, num_invalidates, num_cache_hits,
                 num_cache_misses, hit_ratio, miss_ratio,
                 num_evictions, num_writebacks):
        self.total_cache_accesses = total_cache_accesses
        self.num_cache_reads = num_cache_reads
        self.num_cache_writes = num_cache_writes
        self.num_invalidates = num_invalidates
        self.num_cache_hits = num_cache_hits
        self.num_cache_misses = num_cache_misses
        self.hit_ratio = hit_ratio
        self.miss_ratio = miss_ratio
        self.num_evictions = num_evictions
        self.num_writebacks = num_writebacks

    def print_output(self):
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
