from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
from argparse import ArgumentParser
from cache import Cache
from summary import Summary


class CacheSimulation(object):
    """Cache Simulation"""

    def main(self):
        args = self.parse_args(sys.argv[1:])
        try:
            self.validate_args(args)
        except (IOError, ValueError) as e:
            print("\nError: {}".format(e))
            sys.exit(1)
        self.start_simulation(args)

    def parse_args(self, args):

        arg_parser = ArgumentParser(
            add_help=True,
            description="Parse args for Cache Simulation")

        arg_parser.add_argument(
            "-f", "--input-trace-file-path",
            help="Input Trace File Path",
            dest="input_trace_file_path", default=None, required=True)

        arg_parser.add_argument(
            "-s", "--num-sets",
            help="Number of Cache Line Sets",
            dest="num_sets", type=int, default=None, required=True)

        arg_parser.add_argument(
            "-w", "--num-ways",
            help="Number Ways",
            dest="num_ways", type=int, default=None, required=True, choices=[1,2,4,8])

        arg_parser.add_argument(
            "-l", "--line-size",
            help="Cache Line Size",
            dest="line_size", type=int, default=None, required=True, choices=[32,64,128])

        arg_parser.add_argument(
            "-r", "--replacement-policy",
            help="Replacement Policy should be either 0=True LRU or 1=1-Bit LRU",
            dest="replacement_policy", type=int, default=0, choices=[0,1])

        return arg_parser.parse_args(args)


    def validate_args(self, args):
        """validate the args"""

        def isPowerOfTwo(x):
            return x and (not (x & (x - 1)))

        if not isPowerOfTwo(args.num_sets):
            print("num_sets is not power of 2")
            sys.exit(1)

        # check input_trace_file_path exists
        input_trace_file_path = args.input_trace_file_path
        if input_trace_file_path is not None:
            if not os.path.exists(input_trace_file_path):
                raise IOError("The input_trace_file_path {} "
                              "does not exist".
                              format(input_trace_file_path))


    def start_simulation(self, args):
        # Create a Cache based of configuration
        cache = Cache(args.num_sets,
                         args.num_ways,
                         args.line_size,
                         args.replacement_policy)

        # cache.show_cache()

        # output summary
        summary = Summary()
        # print('Loading tracefile...')
        trace_file = open(args.input_trace_file_path, "r")
        for line in trace_file.read().splitlines():
            line_info = line.split()
            access_type = int(line_info[0])
            hex_address = line_info[1]
            cache.process_cache(access_type, hex_address, summary)

        # cache.show_cache()
        summary.print_output()

if __name__ == "__main__":
    util = CacheSimulation()
    util.main()
