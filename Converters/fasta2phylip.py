#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python2 and Python3 compatible
# Author: Jin


"""
Convert FASTA format file to Phylip format file.

Usage: python fasta2phylip.py fasta_file.phy
"""

from __future__ import print_function

import os
import sys

__version__ = '1.0.2'


def get_seq_list_from_fasta(file_name):
    """Get titles and single-line seqs from fasta file.

    Example:
        FASTA file:
            > title_1
            ATGC
            GC
            > title_2
            GCAT
            AT

        Return:
            (["title_1", "title_2"], ['ATGCGC', 'GCATAT'])
    """
    with open(file_name, 'r') as f:
        lines = f.readlines()
    title_list = []
    long_seq_list = []
    temp_string = ''
    for line in lines:
        if line.startswith('>'):
            title_list.append(line)
            long_seq_list.append(temp_string)
            temp_string = ''
        else:
            temp_string += line.replace('\n', '')\
                .replace(' ', '').replace('\t', '')
    long_seq_list.append(temp_string)
    long_seq_list = long_seq_list[1:]
    title_list = [x.strip() for x in title_list]
    long_seq_list = [x.strip() for x in long_seq_list]

    return title_list, long_seq_list


def convert_fasta_to_phylip(in_file):
    """
    Convert fasta format to phylip format
    """
    title_list, seq_list = get_seq_list_from_fasta(in_file)
    title_num = len(title_list)
    seq_length = len(seq_list[0])
    print("[Length of species]   -->  %d" % title_num)
    print("[Length of sequence]  -->  %d" % seq_length)
    longest_title_length = 0
    for i in title_list:
        if len(i) > longest_title_length:
            longest_title_length = len(i)
    final_string = ''
    final_string += '%d  %d\n\n' % (title_num, seq_length)
    for i, title in enumerate(title_list):
        final_string += '%s%s%s\n' % (
            title.replace('>', '').replace(' ', '_').strip(),
            ' '*(longest_title_length-len(title.strip())+5),
            seq_list[i].strip())
        print("  [%d]  -  %s" % (i+1, title.replace('>', '')))

    out_file = in_file + '.phy'
    with open(out_file, 'w') as f:
        try:
            f.write(final_string)
            print('[Written]  -->  %s' % out_file)
        except IOError as e:
            print("Cannot write to %s: %s" % (
                out_file, e))


def main():
    arg_list = sys.argv
    usage_info = 'Usage: python fasta2phylip.py fasta_file.phy'
    if len(arg_list) != 2:
        sys.exit('[ERROR] Argument number must be 2.\n%s' % usage_info)
    if not os.path.isfile(arg_list[-1]):
        sys.exit('[ERROR] FASTA file does not exist: %s.\n%s' %
                 (arg_list[-1], usage_info))
    in_file = sys.argv[-1]
    convert_fasta_to_phylip(in_file=in_file)


if __name__ == '__main__':
    main()
