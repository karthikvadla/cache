from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import math
from set import Set

class Cache(object):
    """Cache data structure"""

    def __init__(self, num_sets, num_ways, line_size, replacement_policy):
        self.num_sets = num_sets
        self.num_ways = num_ways
        self.line_size = line_size
        self.replacement_policy = replacement_policy
        self.sets = [Set(num_ways, line_size) for i in range(num_sets)]


    def process_cache(self, access_type, hex_address, summary):
        # print("=======================================================")
        # print("hex_address: {}".format(hex_address))
        tag_bits, index_bits = self.get_tag_and_index_bits(hex_address)
        tag_address = self.bin_to_hex(tag_bits)
        line_index = int(index_bits, 2)
        # print("tag_bits: {}".format(tag_bits))
        # print("tag_address: {}".format(tag_address))
        # print("index_bits: {}".format(index_bits))
        # print("line_index: {}".format(line_index))

        if self.num_ways == 1:
            self.directed_map(access_type, line_index, tag_address, summary)

    def invoke_access_type(self, access_type, line_index, tag_address, summary):
        if access_type == 0:
            self.read(line_index, tag_address, summary)
        elif access_type == 1:
            self.write(line_index, tag_address, summary)
        elif access_type == 2:
            self.invalidate(line_index, tag_address, summary)
        else:
            raise ValueError("access_type should be one of [0,1,2]")

    def directed_map(self, access_type, line_index, tag_address, summary):
        self.invoke_access_type(access_type, line_index, tag_address, summary)

    def nway_associative(self):
        pass

    def read(self, set_index, tag_address, summary):
        indexed_set = self.sets[set_index]
        for i in range(len(indexed_set.lines)):
            summary.total_cache_accesses += 1
            if self.sets[set_index].lines[i].valid == 0:
                self.sets[set_index].lines[i].tag = tag_address
                self.sets[set_index].lines[i].valid = 1

                # update statistics
                summary.num_cache_misses += 1
                summary.num_cache_reads += 1
            else:
                if self.sets[set_index].lines[i].tag == tag_address:

                    # update statistics
                    summary.num_cache_hits += 1
                    summary.num_cache_reads += 1
                else:

                    # update statistics
                    summary.num_cache_misses += 1
                    summary.num_cache_reads += 1

                    if self.sets[set_index].lines[i].dirty == 1:
                        summary.num_writebacks += 1
                        self.sets[set_index].lines[i].dirty = 0

                    summary.num_evictions += 1
                    self.sets[set_index].lines[i].tag = tag_address

    def write(self, set_index, tag_address, summary):
        indexed_set = self.sets[set_index]
        for i in range(len(indexed_set.lines)):
            summary.total_cache_accesses += 1
            if self.sets[set_index].lines[i].valid == 0:
                self.sets[set_index].lines[i].tag = tag_address
                self.sets[set_index].lines[i].valid = 1
                self.sets[set_index].lines[i].dirty = 1

                # update statistics
                summary.num_cache_misses += 1
                summary.num_cache_writes += 1
            else:
                if self.sets[set_index].lines[i].tag == tag_address:

                    # update statistics
                    summary.num_cache_hits += 1
                    summary.num_cache_writes += 1
                    self.sets[set_index].lines[i].dirty = 1
                else:

                    # update statistics
                    summary.num_cache_misses += 1
                    summary.num_cache_writes += 1

                    if self.sets[set_index].lines[i].dirty == 1:
                        summary.num_writebacks += 1
                        self.sets[set_index].lines[i].dirty = 0
                    else:
                        self.sets[set_index].lines[i].dirty = 1

                    summary.num_evictions += 1
                    self.sets[set_index].lines[i].tag = tag_address

    def invalidate(self, set_index, tag_address, summary):
        indexed_set = self.sets[set_index]
        for i in range(len(indexed_set.lines)):
            summary.total_cache_accesses += 1
            if self.sets[set_index].lines[i].valid == 1:
                if self.sets[set_index].lines[i].tag == tag_address:
                    self.sets[set_index].lines[i].valid = 0

            summary.num_invalidates += 1

    def bin_to_hex(self, binary):
        return '{:08X}'.format(int(binary, 2))

    def get_tag_and_index_bits(self, hex_address):
        index = int(math.log(self.num_sets, 2))
        byte_select = int(math.log(self.line_size, 2))
        binary = bin(int(hex_address,16))[2:].zfill(32)
        # print("Binary representation: {}".format(binary))
        tag_bits = binary[:(len(binary) - index - byte_select)]
        rest_bits = binary[(len(binary) - index - byte_select):]
        index_bits = rest_bits[:index]
        return tag_bits, index_bits

    def show_cache(self):
        """Display Cache information"""
        print("===== Simulated cache with below configuration =====")
        print("num_sets: {}".format(self.num_sets))
        print("num_ways: {}".format(self.num_ways))
        print("line_size: {}".format(self.line_size))
        print("Replacement: {}".format(self.replacement_policy))
        print("Valid\t Dirty\t Tag")
        for line in self.lines:
            print(str(line.valid) + "\t " + str(line.dirty) + "\t " + str(line.tag))
