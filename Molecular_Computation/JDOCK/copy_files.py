#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Copy *.mol2 files to each folder, generate *_dock.in files."""

from __future__ import print_function

import os
import re
from shutil import copyfile

mol2_file_name = 'gan1.mol2'
error_list = []


def list_dirs():
    return [name for name in os.listdir(".") if os.path.isdir(name)]


def get_first_dock_in_file(dir_name):
    all_dock_in_files = [name for name in os.listdir(dir_name)
                         if name.endswith("dock.in")]
    if not all_dock_in_files:
        error_list.append('--> NO dock.in file: %s' % dir_name)
        return ''
    return all_dock_in_files[0]


def modify_dock_in_file(dock_in_file_name, mol2_file_name):
    with open(dock_in_file_name, 'r') as f:
        lines = f.readlines()
    exists_name_re = re.compile("\S+.mol2")
    try:
        exists_name = exists_name_re.findall(lines[0])[0]
    except:
        error_list.append(dock_in_file_name)
        return ''
    else:
        lines[0] = lines[0].replace(exists_name, mol2_file_name)
        lines[1] = lines[1].replace(exists_name.strip('.mol2'),
                                    mol2_file_name.strip('.mol2'))
        return ''.join(lines)


def main():
    protern_dirs = list_dirs()
    for i, each_dir in enumerate(protern_dirs):
        one_dock_in_file = get_first_dock_in_file(each_dir)
        if not one_dock_in_file:
            print("%4d :  ERROR" % (i+1))
            continue
        print("%4d :  %s  |  %s" % (i+1, each_dir, one_dock_in_file))
        out_file = os.path.join(each_dir,
                                mol2_file_name.strip('.mol2')+'_dock.in')
        copyfile(mol2_file_name, os.path.join(each_dir, mol2_file_name))
        with open(out_file, 'w') as f:
            f.write(modify_dock_in_file(
                    os.path.join(each_dir,
                                 one_dock_in_file),
                    mol2_file_name))
    with open("error2016.txt", 'w') as f:
        f.write('\n'.join(error_list))


if __name__ == '__main__':
    main()
