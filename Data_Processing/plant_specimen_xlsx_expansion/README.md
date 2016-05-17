Plant specimen xlsx expansion script
====================================

This script is used to expand plant specimen record lines to corresponding numbers for specimen label printing.

Prerequisites
-------------

You need to download and install [Python](https://www.python.org/downloads/) to run this script (Both Python2 and Python3 are supported).

Usage
-----

Open a terminal or Command Prompt, type this:

    python expand_specimen_numbers.py input.xlsx output.xlsx

For example
-----------

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

Notice
------

This script determines the columns we need according to the title name of the column ("`物种编号`" and "`份数`"). Order is not important once you name the columns correctly.
