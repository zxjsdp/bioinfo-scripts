#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Select lines randomly from source matrix and generate files.

PREPARATION:
------------

You need two files:

1. data.csv
   data.csv is csv file that contains the data matrix.
   WARNING: only data, not any header.

                         group_1               group_2         ...
                           |                      |
                      +----+-----+            +---+---+
                      |          |            |       |
                    id_1        id_2        id_3    id_4       ...
                +----------+-----------+-----------+----------
   component_1  |    2     |     8     |     7     |  ...
   component_1  |    5     |     7     |     9     |  ...
   component_1  |    0     |     0     |     8     |  ...
   component_1  |    8     |     1     |     0     |  ...
   component_1  |    1     |     2     |     0     |  ...
   ...          |   ...    |    ...    |    ...    |  ...

2. header.txt
   header.txt is text file that has each component as one line.

./
 |__ random_sample.py
 |
 |__ data.csv
 |
 |__ header.txt


AFTER RUNNING:
--------------

./
 |__ sample/
 |   |__ 0.csv
 |   |__ 1.csv
 |   |__ 2.csv
 |   |__ 3.csv
 |   |__ ...
 |
 |__ random_list_log.txt

After running, there will be a new folder named "sample" generated for you.
All sample csv files can be found there.

And a "random_list_log.txt" file will be generated for you. This file is
important for you because if you find any interesting thing if the PDF or PNG
files, you need to check this log file to see what it was.

(DO NOT DELETE IT UNLESS YOU KNOW WHAT YOU ARE DOING!)


NEXT STEP:
----------

Then you can run next python script to do PCA automatically:

    python run_r.py

"""

from __future__ import print_function, division

import os
import random

__version__ = '0.1'

# ============================================================================
# You can change these parameters as you wish
# ============================================================================

# How many components do you need
SAMPLE_LINE = 20

# How many csv sample files do you need
SAMPLE_TIMES = 100

# Data file
TEST_DATA = 'data_no_header.csv'

# Header text file.
TITLE_FILE = 'header.txt'

# ============================================================================
# You don't need to change parameters below, unless you know
# what you are doing
# ============================================================================

# The ouput folder for sample csv files. The files will be used for run_r.py
OUT_FOLDER = 'sample'


def get_random_list(total_line_num, sample_num):
    """Return a list of unique rondom number for given total number.

    >>> out = get_random_list(50, 10)
    >>> 0 <= out[1] <= 50
    True
    >>> len(out) == 10
    True
    """
    random_list = random.sample(range(total_line_num), sample_num)
    return random_list


def read_file(file_name):
    """Read file and return a list of lines.

    Example:
        ['1,2,3', '4,5,6', '7,8,9']

    >>> out = read_file(TEST_DATA)
    >>> len(out) == 16
    True
    >>> out[0]
    '1,2,3,4,5,6,7,8,9,10,11,12'
    """
    with open(file_name, 'r') as f:
        list_of_lines = [_.strip() for _ in f.readlines() if _.strip()]
    return list_of_lines


def get_titles(title_file=TITLE_FILE):
    """Read title text file and return a list of titles."""
    with open(title_file, 'r') as f:
        return [x.strip() for x in f.readlines()]


def generate_sample(list_of_lines, all_title_list):
    """Generate sample files."""
    random_log_list = []
    out_dir = os.path.join(os.getcwd(), OUT_FOLDER)
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    for i in range(SAMPLE_TIMES):
        print("[ %-3d ] Generating random file..." % (i + 1))
        sample_file_name = '%s.csv' % i
        random_list = get_random_list(len(list_of_lines),
                                      sample_num=SAMPLE_LINE)
        title_list = [all_title_list[x] for x in random_list]

        # Write random list to log
        random_log_list.append('\n%s\n[Sample]  %s\n' % ('='*62, i+1))
        for i, each in enumerate(random_list):
            random_log_list.append('%3s - [ %-3s ] - %s'
                                   % (i+1, random_list[i], title_list[i]))

        selected_lines = [list_of_lines[x] for x in random_list]
        list_of_list = [x.split(',') for x in selected_lines]
        reversed_matrix = [[r[col] for r in list_of_list]
                           for col in range(len(list_of_list[0]))]

        with open(os.path.join(out_dir, sample_file_name), 'w') as f:
            f.write(','.join(title_list)
                    + '\n'
                    + '\n'.join([','.join(x) for x in reversed_matrix]))

    with open('random_list_log.txt', 'w') as f:
        f.write('\n'.join(random_log_list))


def main():
    """Do main job."""
    list_of_lines = read_file(file_name=TEST_DATA)
    all_title_list = get_titles(title_file=TITLE_FILE)
    generate_sample(list_of_lines, all_title_list)
    print('\n%s' % ('-' * 62))
    print("Total sample files:         %s" % SAMPLE_TIMES)
    print("Lines in each sample file:  %s" % SAMPLE_LINE)
    print('%s' % ('-' * 62))


def doctest_main():
    """Doctest main."""
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    # doctest_main()
    main()
