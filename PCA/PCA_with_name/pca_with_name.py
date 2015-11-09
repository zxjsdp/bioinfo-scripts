#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Do Principal Component Analysis and draw plot with name."""


from __future__ import print_function

import os
import sys
from subprocess import Popen


# ============================================================================
# You can change these parameters as you wish
# ============================================================================

# A vector of row names. (Names you want to display in the plot for each dot)
#     [ EXAMPLE 1 ]  'c(1:22)'
#     [ EXAMPLE 2 ]  'c("name1", "name2", "name3", ...)'
#     [ EXAMPLE 3 ]  'c(paste('name', 1:22, sep="-"))'
ROW_NAMES = 'c(1:22)'


# The column that contains group information.
#
#           1           2           3                    21         <---
#       Component1    Comp2       Comp3      ...        Group
#      +----------+-----------+-----------+----------+----------+
#   1  |    2     |     8     |     7     |  ...     |    G1    |
#   2  |    5     |     7     |     9     |  ...     |    G1    |
#   3  |    0     |     0     |     8     |  ...     |    G1    |
#   4  |    8     |     1     |     0     |  ...     |    G2    |
#   5  |    1     |     2     |     0     |  ...     |    G3    |
#   ...|   ...    |    ...    |    ...    |  ...     |    G4    |

GROUP_INDEX_LINE = '21'


# ============================================================================
# You don't need to change parameters below, unless you know
# what you are doing
# ============================================================================

TEMPLATE_FILE = 'template_pca_with_name.r'
WORKING_DIR = os.getcwd()


def generate_r_script(csv_file, template_string):
    """Generate R script for current PCA."""
    out_r_script_name = csv_file.rpartition('.')[0] + '.r'
    out_pdf_file = csv_file.rpartition('.')[0] + '.pdf'
    out_png_file = csv_file.rpartition('.')[0] + '.png'

    new_r_string = (
        template_string
        .replace('WORKING_DIR', WORKING_DIR)
        .replace("CSV_FILE", csv_file)
        .replace('ROW_NAMES', ROW_NAMES)
        .replace('GROUP_INDEX_LINE', GROUP_INDEX_LINE)
        .replace('OUT_PDF_PATH', out_pdf_file)
        .replace('OUT_PNG_PATH', out_png_file)
        .replace('\\', '/')
        )

    with open(out_r_script_name, 'wb') as f:
        f.write(new_r_string)
        print("[ INFO ]  Generate R script successfully.")

    return out_r_script_name


def get_template_string():
    """Open template R script file and return content as string."""
    with open(TEMPLATE_FILE, 'r') as f:
        return f.read()


def get_csv_file():
    """Get csv file name from command line argument."""
    arg_list = sys.argv
    if len(arg_list) != 2:
        sys.exit('[ ERROR ]  Invalid parameter number.\n'
                 '[ USAGE ]  python *.py data.csv')
    return arg_list[-1]


def run_r_script():
    """Run the R script generated just now."""
    template_string = get_template_string()
    csv_file = get_csv_file()
    out_r_file = generate_r_script(csv_file, template_string)

    Popen(
        ['R',
         'CMD',
         'BATCH',
         out_r_file],
        shell=True)
    print("[ INFO ]  Run R script successfully.")
    print("\n--->  Please check files:\n\n"
          "    Rplots*.pdf\n    Rplots*.png")


def main():
    run_r_script()


if __name__ == '__main__':
    main()
