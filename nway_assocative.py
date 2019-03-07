import time

class NWayAssociative(object):
    """N way Associative implementation"""

    @staticmethod
    def read(sets, set_index, tag_address, replacement_policy, summary):
        indexed_set = sets[set_index]
        summary.total_cache_accesses += 1
        if all(line.valid == 0 for line in indexed_set.lines):
            sets[set_index].lines[0].tag = tag_address
            sets[set_index].lines[0].valid = 1
            if replacement_policy == 1:
                sets[set_index].lines[0].mru = 1
            else:
                sets[set_index].lines[0].mru = time.time()
                # update statistics
            summary.num_cache_misses += 1
            summary.num_cache_reads += 1
        else:
            first_time = True
            index_flag = -1
            for i in range(len(indexed_set.lines)):
                if sets[set_index].lines[i].valid == 1:
                    if sets[set_index].lines[i].tag == tag_address:
                        # update statistics
                        summary.num_cache_hits += 1
                        summary.num_cache_reads += 1

                        if replacement_policy == 0:
                            sets[set_index].lines[0].mru = time.time()

                        break
                    else:
                        continue
                else:
                    if first_time:
                        index_flag = i
                        first_time = False
                    continue

            if index_flag != -1:
                 sets[set_index].lines[index_flag].tag = tag_address
                 sets[set_index].lines[index_flag].valid = 1
                 if replacement_policy == 1:
                     sets[set_index].lines[index_flag].mru = 1
                 else:
                     sets[set_index].lines[index_flag].mru = time.time()

                 # update statistics
                 summary.num_cache_misses += 1
                 summary.num_cache_reads += 1
            else:
                 if replacement_policy == 1:
                     for i in range(len(indexed_set.lines)):
                         sets[indexed_set].lines[i].mru = 0

                     sets[set_index].lines[0].tag = tag_address
                     sets[set_index].lines[0].mru = 1
                     if sets[set_index].lines[0].dirty == 1:
                        summary.num_writebacks += 1
                        sets[set_index].lines[0].dirty = 0

                     summary.num_cache_misses += 1
                     summary.num_cache_reads += 1
                     summary.num_evictions += 1
                 else:
                     min_index = 0
                     min_time = time.time()
                     for i in range(len(indexed_set.lines)):
                         if sets[indexed_set].lines[i].mru < min_time:
                            min_index = i
                            min_time = sets[indexed_set].lines[i].mru

                     sets[set_index].lines[min_index].tag = tag_address
                     sets[set_index].lines[min_index].mru = time.time()
                     if sets[set_index].lines[0].dirty == 1:
                         summary.num_writebacks += 1
                         sets[set_index].lines[min_index].dirty = 0

                     summary.num_cache_misses += 1
                     summary.num_cache_reads += 1
                     summary.num_evictions += 1



    @staticmethod
    def write(sets, set_index, tag_address, replacement_policy, summary):
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
    def invalidate(sets, set_index, tag_address, replacement_policy, summary):
        indexed_set = sets[set_index]
        for i in range(len(indexed_set.lines)):
            summary.total_cache_accesses += 1
            if sets[set_index].lines[i].valid == 1:
                if sets[set_index].lines[i].tag == tag_address:
                    sets[set_index].lines[i].valid = 0

            summary.num_invalidates += 1