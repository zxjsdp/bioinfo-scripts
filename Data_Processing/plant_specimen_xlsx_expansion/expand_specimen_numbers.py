#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Expand plant specimen numbers.

Usage:

    python expand_specimen_numbers.py input.xlsx output.xlsx

What does this script do:

    Original xlsx:

        ZY20150180, 朴树, ..., 10, ...
        ZY20150181, 三角槭, ..., 15, ...

    After:

        ZY20150180-1, 朴树, ..., 10, ...
        ZY20150180-2, 朴树, ..., 10, ...
        ..., ..., ...
        ZY20150180-9, 朴树, ..., 10, ...
        ZY20150180-10, 朴树, ..., 10, ...
        ZY20150181-1, 三角槭, ..., 15, ...
        ZY20150181-2, 三角槭, ..., 15, ...
        ..., ..., ...
        ZY20150181-14, 三角槭, ..., 15, ...
        ZY20150181-15, 三角槭, ..., 15, ...
"""


from __future__ import (print_function, unicode_literals,
                        with_statement)

import os
import sys
import logging
# Use zipimport to satisfy requirements
sys.path.insert(0, 'library.zip')

# Import openpyxl from library.zip. You can also pip install it
import openpyxl


# logging
FILE_HANDLER_FORMAT = ('%(asctime)s [%(levelname)s]  %(message)s')
logging.basicConfig(level=logging.DEBUG,
                    format=FILE_HANDLER_FORMAT,
                    datefmt="%Y-%m-%d %H:%M:%S",
                    filename="log.txt",
                    filemode="w")

# logging handler for displaying output to screen
CONSOLE = logging.StreamHandler()
CONSOLE.setLevel(logging.INFO)
FORMATTER = logging.Formatter('[%(levelname)s]  %(message)s')
CONSOLE.setFormatter(FORMATTER)

logging.getLogger("").addHandler(CONSOLE)


class XlsxFile(object):
    """Handel xlsx files and return a matrix of content."""
    def __init__(self, excel_file):
        try:
            self.workbook = openpyxl.load_workbook(excel_file)
        # Invalid xlsx format
        except openpyxl.utils.exceptions.InvalidFileException as e:
            logging.error("Invalid xlsx format. (%s)" % e)
            sys.exit(1)
        except IOError as e:
            logging.error("No such xlsx file: %s. (%s)" % (excel_file, e))
            sys.exit(1)
        except BaseException as e:
            logging.error(e)
            sys.exit(1)

        # self.ws = self.wb.get_active_sheet()
        self.active_sheet = self.workbook.active
        self.ws_title = self.active_sheet.title
        self.matrix = []
        self._get_matrix()

    def _get_matrix(self):
        """Get a two dimensional matrix from the xlsx file."""
        for row in self.active_sheet.rows:
            row_container = []
            for cell in row:
                row_container.append(cell.value)
            self.matrix.append(tuple(row_container))


def expand_numbers(xlsx_matrix):
    """Expand numbers.

    [Original]

        [
            (ZY20150180, 朴树, ..., 10, ...),
            (ZY20150181, 三角槭, ..., 15, ...),
        ]

    [After expansion]

        [
            (ZY20150180-1, 朴树, ..., 10, ...),
            (ZY20150180-2, 朴树, ..., 10, ...),
            (..., ..., ...),
            (ZY20150180-9, 朴树, ..., 10, ...),
            (ZY20150180-10, 朴树, ..., 10, ...),

            (ZY20150181-1, 三角槭, ..., 15, ...),
            (ZY20150181-2, 三角槭, ..., 15, ...),
            (..., ..., ...),
            (ZY20150181-14, 三角槭, ..., 15, ...),
            (ZY20150181-15, 三角槭, ..., 15, ...),
        ]
    """
    out_tuple_list = []
    for i, each_tuple in enumerate(xlsx_matrix):
        if i == 0:
            species_code_index = each_tuple.index('物种编号')
            copy_number_index = each_tuple.index('份数')
            title_line_list = list(each_tuple)
            title_line_list.insert(species_code_index + 1, '编号')
            out_tuple_list.append(tuple(title_line_list))
        else:
            species_code = each_tuple[species_code_index]
            copy_number = int(each_tuple[copy_number_index])
            for j in range(copy_number):
                line_list = list(each_tuple)
                line_list.insert(species_code_index + 1, '%s-%d' %
                                 (species_code, j + 1))
                out_tuple_list.append(tuple(line_list))

    return out_tuple_list


def write_to_xlsx_file(out_tuple_list, xlsx_outfile_name):
    """Write tuple list to xlsx file.
    >>> write_to_xlsx_file([('a', 'b', 'c'), ('e', 'f', 'g')])
    +-----+-----+-----+
    |  a  |  b  |  c  |
    +-----+-----+-----+
    |  e  |  f  |  g  |
    +-----+-----+-----+
    """
    out_wb = openpyxl.Workbook()

    ws1 = out_wb.active
    ws1.title = "Specimen"

    # # Header
    # ws1.append(HEADER_TUPLE)

    # Content
    for tuple_row in out_tuple_list:
        ws1.append(tuple_row)
    try:
        out_wb.save(filename=xlsx_outfile_name)
        logging.info("The result was saved to xlsx file: %s" %
                     xlsx_outfile_name)
    except IOError as e:
        basename, _, ext = xlsx_outfile_name.rpartition(".")
        alt_xlsx_outfile = "%s.alt.%s" % (basename, ext)
        logging.info("[ xlsx File ]  Saved results to %s" % alt_xlsx_outfile)
        logging.error(" *  [PERMISSION DENIED] Is file open: %s? (%s)" %
                      (xlsx_outfile_name, e))
        out_wb.save(filename=alt_xlsx_outfile)
        logging.warning("The result was saved to another file: %s" %
                        alt_xlsx_outfile)


def main():
    """Main func"""
    arg_list = sys.argv
    if len(arg_list) != 3:
        logging.error("Usage: python expand_specimen_numbers.py "
                      "input.xlsx output.xlsx")
        sys.exit(1)
    if not os.path.isfile(arg_list[1]):
        logging.error("Input file does not exist: %s" % arg_list[1])
        sys.exit(1)

    xlsx_matrix = XlsxFile(arg_list[1]).matrix
    out_tuple_list = expand_numbers(xlsx_matrix)
    write_to_xlsx_file(out_tuple_list, arg_list[2])


if __name__ == '__main__':
    main()
