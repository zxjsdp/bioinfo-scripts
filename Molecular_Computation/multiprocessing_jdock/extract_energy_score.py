#!/usr/bin/env python
# -*- coding: utf-8 -*0

"""Extract and sort Energy Score, protein name, M-Score, and X-Score

Energy Score:          -34.372932
         vdw:          -25.955530
          es:           -8.417400
M-Score:            -215.497467
X-Score:               5.020359

Energy Score    Name        M-Score         X-Score
-34.372932      1H1H       -215.497467      5.020359
-34.372932      1H2H       -215.497467      5.020359
-34.372932      1H1H       -215.497467      5.020359
-34.372932      1H1H       -215.497467      5.020359
-34.372932      1H1H       -215.497467      5.020359
-34.372932      1H1H       -215.497467      5.020359
"""

import os


def find_by_keywords(filename):
    with open(filename, 'r') as f:
        energy_score, m_score, x_score = '0', '0', '0'
        for line in f:
            line = line.strip()
            if line.startswith('Energy Score'):
                energy_score = line.split()[-1]
            if line.startswith('M-Score'):
                m_score = line.split()[-1]
            if line.startswith('X-Score'):
                x_score = line.split()[-1]
    return energy_score, m_score, x_score


def extract_energy_scores():
    unsorted_tuple_list = []
    all_files = [x for x in os.listdir('.') if x.endswith('.in')]
    for i, each_file in enumerate(all_files):
        prot_name = each_file.split('.')[0]
        energy_score, m_score, x_score = find_by_keywords(each_file)
        energy_score = float(energy_score)
        unsorted_tuple_list.append((energy_score, prot_name, m_score, x_score))
    return unsorted_tuple_list


def sort_by_energy_score(unsorted_tuple_list):
    return sorted(unsorted_tuple_list, key=lambda x: x[0])


def main():
    unsorted_tuple_list = extract_energy_scores()
    sorted_tuple_list = sort_by_energy_score(unsorted_tuple_list)
    with open('_sorted_energy_scores.txt', 'w') as f:
        f.write('\n'.join(['\t'.join([str(y) for y in x]) for x in sorted_tuple_list]))


if __name__ == '__main__':
    main()
