from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import math
from set import Set
from directed import DirectedMap
from nway_assocative import NWayAssociative

class Cache(object):
    """Cache data structure"""

    def __init__(self, num_sets, num_ways, line_size, replacement_policy):
        self.num_sets = num_sets
        self.num_ways = num_ways
        self.line_size = line_size
        self.replacement_policy = replacement_policy
        self.sets = [Set(num_ways, replacement_policy) for i in range(num_sets)]


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
        self.invoke_access_type(access_type, line_index, tag_address, self.replacement_policy, summary)

    def invoke_access_type(self, access_type, line_index, tag_address, replacement_policy, summary):
        if access_type == 0:
            if self.num_ways == 1:
                DirectedMap().read(self.sets, line_index, tag_address, summary)
            else:
                NWayAssociative().read(self.sets,line_index, tag_address, replacement_policy, summary)
        elif access_type == 1:
            if self.num_ways == 1:
                DirectedMap().write(self.sets,line_index, tag_address, summary)
            else:
                NWayAssociative().write(self.sets,line_index, tag_address, replacement_policy, summary)
        elif access_type == 2:
            if self.num_ways == 1:
                DirectedMap().invalidate(self.sets,line_index, tag_address, summary)
            else:
                NWayAssociative().invalidate(self.sets,line_index, tag_address, replacement_policy, summary)
        else:
            raise ValueError("access_type should be one of [0,1,2]")


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
