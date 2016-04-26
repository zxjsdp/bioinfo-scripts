#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Run jdock with multiprocess."""

from __future__ import with_statement, print_function

import os
import sys
import time
import signal
from multiprocessing import Pool
from subprocess import Popen, PIPE


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
MOL2_FILE_NAME = 'glycyrrhizicacid.mol2'
PROCESS_NUM = 8
LIMIT = 500
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

COUNT = 0
CURRENT_PATH = os.getcwd()
BASENAME = MOL2_FILE_NAME.strip('.mol2')
KEYWORDS_TUPLE = ('Energy Score', "M-Score", "X-Score")


def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def detect_incomplete_file(out_file):
    incomplete = 0
    with open(out_file, 'r') as f:
        content = f.read()
    for each_keyword in KEYWORDS_TUPLE:
        if each_keyword not in content:
            incomplete = 1
    if incomplete:
        print('    -> Incomplete outcom will be recomputed: %s' % out_file)
        os.remove(out_file)


def get_all_dir_name_list():
    """Get a list of proterin directories."""
    dock_in_file = '%s_dock.in' % BASENAME
    all_dirs = [x for x in os.listdir('.') if os.path.isdir(x)]
    print('all_dirs: %d' % len(all_dirs))
    return all_dirs


def single_work(protein_name):
    """Single job for multiprocessing."""
    global COUNT
    COUNT += 1
    dock_in_file = '%s_dock.in' % BASENAME
    jdock_exe_path = '/home/program/JDOCK/jdock/jdock'
    out_folder = os.path.join('_jdock_out', BASENAME)
    out_file = '%s.in' % protein_name
    prot_dir = os.path.join(CURRENT_PATH, protein_name)

    if not os.path.isdir(out_folder):
        os.mkdir(out_folder)

    os.chdir(prot_dir)
    out_file_path = os.path.join('../_jdock_out/', BASENAME, out_file)
    if os.path.isfile(out_file_path):
        detect_incomplete_file(out_file_path)
    if not os.path.isfile(out_file_path):
        print('    Current dir: %s' % os.getcwd())
        if os.path.isfile(dock_in_file):
            print('%d * %s | %s' % (COUNT, PROCESS_NUM, protein_name))
            print('    OUTFILE: %s' % out_file_path)
            out = Popen([jdock_exe_path,
                         '-i', dock_in_file,
                         '-o', out_file_path],
                        shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            print(out.communicate()[0])
        else:
            print('    No dock in file in dir: %s' % protein_name)
    else:
        print('    -> already exists: %s' % protein_name)
    os.chdir('..')


def run_with_multiprocessing_poll():
    """Run with multiprocessing."""
    try:
        protein_name_list = get_all_dir_name_list()
        pool = Pool(PROCESS_NUM, init_worker)
        pool.map(single_work, protein_name_list)
        if COUNT > LIMIT:
            pool.terminate()
        pool.close()
        pool.join()
    except KeyboardInterrupt:
        pool.terminate()
        pool.join()


def main():
    run_with_multiprocessing_poll()


if __name__ == '__main__':
    main()
