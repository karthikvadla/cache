class DirectedMap(object):
    """Directed Map implementation"""

    @staticmethod
    def read(sets, set_index, tag_address, summary):
        indexed_set = sets[set_index]
        for i in range(len(indexed_set.lines)):
            summary.total_cache_accesses += 1
            if sets[set_index].lines[i].valid == 0:
                sets[set_index].lines[i].tag = tag_address
                sets[set_index].lines[i].valid = 1

                # update statistics
                summary.num_cache_misses += 1
                summary.num_cache_reads += 1
            else:
                if sets[set_index].lines[i].tag == tag_address:

                    # update statistics
                    summary.num_cache_hits += 1
                    summary.num_cache_reads += 1
                else:

                    # update statistics
                    summary.num_cache_misses += 1
                    summary.num_cache_reads += 1

                    if sets[set_index].lines[i].dirty == 1:
                        summary.num_writebacks += 1
                        sets[set_index].lines[i].dirty = 0

                    summary.num_evictions += 1
                    sets[set_index].lines[i].tag = tag_address

    @staticmethod
    def write(sets, set_index, tag_address, summary):
        indexed_set = sets[set_index]
        for i in range(len(indexed_set.lines)):
            summary.total_cache_accesses += 1
            if sets[set_index].lines[i].valid == 0:
                sets[set_index].lines[i].tag = tag_address
                sets[set_index].lines[i].valid = 1
                sets[set_index].lines[i].dirty = 1

                # update statistics
                summary.num_cache_misses += 1
                summary.num_cache_writes += 1
            else:
                if sets[set_index].lines[i].tag == tag_address:

                    # update statistics
                    summary.num_cache_hits += 1
                    summary.num_cache_writes += 1
                    sets[set_index].lines[i].dirty = 1
                else:

                    # update statistics
                    summary.num_cache_misses += 1
                    summary.num_cache_writes += 1

                    if sets[set_index].lines[i].dirty == 1:
                        summary.num_writebacks += 1
                        sets[set_index].lines[i].dirty = 0
                    else:
                        sets[set_index].lines[i].dirty = 1

                    summary.num_evictions += 1
                    sets[set_index].lines[i].tag = tag_address
    @staticmethod
    def invalidate(sets, set_index, tag_address, summary):
        indexed_set = sets[set_index]
        for i in range(len(indexed_set.lines)):
            summary.total_cache_accesses += 1
            if sets[set_index].lines[i].valid == 1:
                if sets[set_index].lines[i].tag == tag_address:
                    sets[set_index].lines[i].valid = 0

            summary.num_invalidates += 1