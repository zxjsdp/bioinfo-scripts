Modify fdi file color with given data
=====================================

Modify color, proportion of sector, and max node size of fdi file with given proportion data and fdi file.

Usage
-----

1. Open an terminal
2. Type: `python modify_fdi_file_color_with_given_data.py`

MIN_LIMIT & MAX_LIMIT
---------------------

    if num > MIN_LIMIT:
        num = MIN_LIMIT
    elif num < MAX_LIMIT:
        num = int(round(MAX_LIMIT))
    else:
        num = int(round(num))
