#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Run multiple R script automatically and do PCA, genarating PDF files.

PREPARATION:
------------

You need to install R for PCA analysis. And two additional packages required:

1. devtools

    install.packages('devtools')

2. ggbiplot

    library(devtools)
    install_github("vqv/ggbiplot")

./
 |__ run_r.py
 |
 |__ sample/
 |   |__ 0.csv
 |   |__ 1.csv
 |   |__ 2.csv
 |   |__ ...
 |
 |__ template.r


AFTER RUNNING:
--------------
./
 |
 |__ R_Scripts/
 |   |__ 0.r
 |   |__ 1.r
 |   |__ 2.r
 |   |__ ...
 |
 |__ PDF/
 |   |__ 0.pdf
 |   |__ 1.pdf
 |   |__ 2.pdf
 |   |__ ...
 |
 |__ PNG/
 |   |__ 0.png
 |   |__ 1.png
 |   |__ 2.png
 |   |__ ...
 |
 |__ log.txt


REFERENCES:
-----------

Please refer to these links if you need:

- [vqv/ggbiplot @ GitHub](https://github.com/vqv/ggbiplot)
- [Computing and visualizing PCA in R](http://www.r-bloggers.com/computing-and-visualizing-pca-in-r/)
"""

from __future__ import print_function

import os
import time
from subprocess import Popen

__version__ = '0.1'

# ============================================================================
# You can change these parameters as you wish
# ============================================================================

# Group parameter
# Default:
#    1:9      |    G1
#    10:22    |    G2
GROUP_V = ('"G1", "G1", "G1", "G1", "G1", "G1", "G1", "G1", "G1", '
           '"G2", "G2", "G2", "G2", "G2", "G2", "G2", "G2", "G2", '
           '"G2", "G2", "G2", "G2"')

# If your CPU is strong enough, you can make this parameter smaller (seconds).
# 0 is not recommended!! It will make your CPU 100% used.
SLEEP_TIME = 0.5


# ============================================================================
# You don't need to change parameters below, unless you know
# what you are doing
# ============================================================================

TEMPLATE_FILE = 'template.r'
SAMPLE_FOLDER = 'sample'
R_SCRITS_FOLDER = 'R_Scripts'
OUT_PDF_FILE = 'PDF'
OUT_PNG_FILE = 'PNG'
CWD = os.getcwd()


def get_template_string():
    """Open template R script file and return content as string."""
    with open(TEMPLATE_FILE, 'r') as f:
        return f.read()


def check_folder_exist(folder_path):
    """Create folder if folder not exists."""
    if not os.path.isdir(folder_path):
        os.mkdir(folder_path)


def generate_r_script(id, template_string):
    """Generate R Script for each csv file from R template."""
    working_dir = os.path.join(CWD, 'sample')
    # Put all new r scripts to a folder to keep clean
    r_scripts_path = os.path.join(CWD, R_SCRITS_FOLDER)
    png_path = os.path.join(CWD, OUT_PNG_FILE)
    pdf_path = os.path.join(CWD, OUT_PDF_FILE)

    check_folder_exist(r_scripts_path)
    check_folder_exist(pdf_path)
    check_folder_exist(png_path)

    new_r_content = (
        template_string
        .replace('WORKING_DIR', working_dir)
        .replace('CSV_FILE', '%s.csv' % id)
        .replace('GROUP_VECTOR', GROUP_V)
        .replace('OUT_PDF_FILE',
                 os.path.join(pdf_path, '%s.pdf' % id))
        .replace('OUT_PNG_FILE',
                 os.path.join(png_path, '%s.png' % id)))

    with open(os.path.join(r_scripts_path, '%s.r' % id), 'w') as f:
        f.write(new_r_content.replace('\\', '/'))


def read_csv_info():
    """Scan the ./Sample/ folder and return ids from csv file names."""
    csv_file_list = [_ for _ in os.listdir(os.path.join(CWD, SAMPLE_FOLDER))
                     if _.endswith('csv')]
    id_list = [_.partition('.')[0] for _ in csv_file_list]
    return id_list


def run_multi_r_scripts():
    """Generate R script for each csv file and run the R script."""
    id_list = read_csv_info()
    template_string = get_template_string()
    for id in id_list:
        print('[ Sample ]  %s' % id)
        # Generate R script for each csv file
        generate_r_script(id, template_string)
        # Run this R script
        Popen(
            ['R',
             'CMD',
             'BATCH',
             os.path.join(CWD, R_SCRITS_FOLDER, '%s.r' % id)],
            shell=True)

        # Sleep is not necessary theoretically. But proper sleep time can
        # precent your CPU load 100%.
        time.sleep(SLEEP_TIME)


def main():
    run_multi_r_scripts()


if __name__ == '__main__':
    main()
