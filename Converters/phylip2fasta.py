#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python2 and Python3 compatible
# Author: Jin


"""
Convert Phylip format file to FASTA format file.

Usage: python phylip2fasta.py phylip_file.phy
"""

from __future__ import print_function

import os
import sys

__version__ = '1.0.0'


def convert_phylip_to_fasta(in_file):
    """
    Convert phylip format to fasta format.
    """
    title_list, seq_list = [], []
    out_list = []
    base_name = in_file.rstrip('.phy')
    out_file = '%s.fasta' % base_name

    with open(in_file, 'r') as f:
        lines = [x.strip() for x in f.readlines()]

    species_num = 0
    for i, line in enumerate(lines[1:]):
        if line:
            species_num += 1
            title, seq = line.split()
            print('  [%s]  %s' % (species_num, title))
            title_list.append(title)
            seq_list.append(seq)

    for i, title in enumerate(title_list):
        out_list.append(">%s\n%s\n" % (title, seq_list[i]))

    print('Convert Phylip to FASTA successfully!')

    with open(out_file, 'w') as f:
        f.write('\n'.join(out_list))
        print("Written: %s." % out_file)


def main():
    arg_list = sys.argv
    usage_info = 'Usage: python phylip2fasta.py phylip_file.phy'
    if len(arg_list) != 2:
        sys.exit('[ERROR] Argument number must be 2.\n%s' % usage_info)
    if not os.path.isfile(arg_list[-1]):
        sys.exit('[ERROR] Phyilp file does not exist: %s.\n%s' %
                 (arg_list[-1], usage_info))
    in_file = sys.argv[-1]
    convert_phylip_to_fasta(in_file=in_file)


if __name__ == '__main__':
    main()
