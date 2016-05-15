#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Processing four region raw data.

[Usage]

    1. open a terminal
    2. type: python modify_fdi_file_color_with_given_data.py

[Rules]

    if num > MIN_LIMIT:
        num = MIN_LIMIT
    elif num < MAX_LIMIT1:
        num = MAX_LIMIT1
    else:
        num = int(num)

"""

from __future__ import print_function

import os
try:
    from PIL import Image, ImageFont, ImageDraw
    import colorsys
except ImportError:
    Image, ImageFont, ImageDraw = None, None, None
    colorsys = None

__version__ = '0.2.0'

IGNORE_LIMIT = 0
MIN_LIMIT = 1
MAX_LIMIT = 700

DATA_FILE = 'frequency.txt'
RAW_DATA_FILE = 'frequency.raw.txt'
INFO_FILE = 'info_1.txt'
FDI_FILE = '1.fdi'


MIN_CIRC_RADIUS = '10'
MAX_CIRC_RADIUS = '100'
BORDER_COLOR = '0'
REGION_LISTS = ['Antarctica', 'Arctic', 'Green', 'Alaska']
COLOR_LIST = [
    ('Green', (0, 128, 0)),
    ('Cyan', (0, 255, 255)),
    ('Purple', (128, 0, 128)),
    ('Orange', (255, 165, 0))
]
INFO_LINE_STYLE = "    %4d / %4d:\t|\t%18s\t|\t%15s\t|\t%18s"

OUT_DIR = os.path.abspath('./output')
IMAGE_DIR = os.path.abspath('./images')
for each_dir in [OUT_DIR, IMAGE_DIR]:
    if not os.path.isdir(each_dir):
        os.mkdir(each_dir)

EXISTS_COLOR_DICT = {}
RGB_TO_COLOR_NAMES = {
    (0, 0, 0): ['Black'],
    (0, 0, 128): ['Navy', 'NavyBlue'],
    (0, 0, 139): ['DarkBlue'],
    (0, 0, 205): ['MediumBlue'],
    (0, 0, 255): ['Blue'],
    (0, 100, 0): ['DarkGreen'],
    (0, 128, 0): ['Green'],
    (0, 139, 139): ['DarkCyan'],
    (0, 191, 255): ['DeepSkyBlue'],
    (0, 206, 209): ['DarkTurquoise'],
    (0, 250, 154): ['MediumSpringGreen'],
    (0, 255, 0): ['Lime'],
    (0, 255, 127): ['SpringGreen'],
    (0, 255, 255): ['Cyan', 'Aqua'],
    (25, 25, 112): ['MidnightBlue'],
    (30, 144, 255): ['DodgerBlue'],
    (32, 178, 170): ['LightSeaGreen'],
    (34, 139, 34): ['ForestGreen'],
    (46, 139, 87): ['SeaGreen'],
    (47, 79, 79): ['DarkSlateGray', 'DarkSlateGrey'],
    (50, 205, 50): ['LimeGreen'],
    (60, 179, 113): ['MediumSeaGreen'],
    (64, 224, 208): ['Turquoise'],
    (65, 105, 225): ['RoyalBlue'],
    (70, 130, 180): ['SteelBlue'],
    (72, 61, 139): ['DarkSlateBlue'],
    (72, 209, 204): ['MediumTurquoise'],
    (75, 0, 130): ['Indigo'],
    (85, 107, 47): ['DarkOliveGreen'],
    (95, 158, 160): ['CadetBlue'],
    (100, 149, 237): ['CornflowerBlue'],
    (102, 205, 170): ['MediumAquamarine'],
    (105, 105, 105): ['DimGray', 'DimGrey'],
    (106, 90, 205): ['SlateBlue'],
    (107, 142, 35): ['OliveDrab'],
    (112, 128, 144): ['SlateGray', 'SlateGrey'],
    (119, 136, 153): ['LightSlateGray', 'LightSlateGrey'],
    (123, 104, 238): ['MediumSlateBlue'],
    (124, 252, 0): ['LawnGreen'],
    (127, 255, 0): ['Chartreuse'],
    (127, 255, 212): ['Aquamarine'],
    (128, 0, 0): ['Maroon'],
    (128, 0, 128): ['Purple'],
    (128, 128, 0): ['Olive'],
    (128, 128, 128): ['Gray', 'Grey'],
    (132, 112, 255): ['LightSlateBlue'],
    (135, 206, 235): ['SkyBlue'],
    (135, 206, 250): ['LightSkyBlue'],
    (138, 43, 226): ['BlueViolet'],
    (139, 0, 0): ['DarkRed'],
    (139, 0, 139): ['DarkMagenta'],
    (139, 69, 19): ['SaddleBrown'],
    (143, 188, 143): ['DarkSeaGreen'],
    (144, 238, 144): ['LightGreen'],
    (147, 112, 219): ['MediumPurple'],
    (148, 0, 211): ['DarkViolet'],
    (152, 251, 152): ['PaleGreen'],
    (153, 50, 204): ['DarkOrchid'],
    (154, 205, 50): ['YellowGreen'],
    (160, 82, 45): ['Sienna'],
    (165, 42, 42): ['Brown'],
    (169, 169, 169): ['DarkGray', 'DarkGrey'],
    (173, 216, 230): ['LightBlue'],
    (173, 255, 47): ['GreenYellow'],
    (175, 238, 238): ['PaleTurquoise'],
    (176, 196, 222): ['LightSteelBlue'],
    (176, 224, 230): ['PowderBlue'],
    (178, 34, 34): ['Firebrick'],
    (184, 134, 11): ['DarkGoldenrod'],
    (186, 85, 211): ['MediumOrchid'],
    (188, 143, 143): ['RosyBrown'],
    (189, 183, 107): ['DarkKhaki'],
    (192, 192, 192): ['Silver'],
    (199, 21, 133): ['MediumVioletRed'],
    (205, 92, 92): ['IndianRed'],
    (205, 133, 63): ['Peru'],
    (208, 32, 144): ['VioletRed'],
    (210, 105, 30): ['Chocolate'],
    (210, 180, 140): ['Tan'],
    (211, 211, 211): ['LightGray', 'LightGrey'],
    (216, 191, 216): ['Thistle'],
    (218, 112, 214): ['Orchid'],
    (218, 165, 32): ['Goldenrod'],
    (219, 112, 147): ['PaleVioletRed'],
    (220, 20, 60): ['Crimson'],
    (220, 220, 220): ['Gainsboro'],
    (221, 160, 221): ['Plum'],
    (222, 184, 135): ['Burlywood'],
    (224, 255, 255): ['LightCyan'],
    (230, 230, 250): ['Lavender'],
    (233, 150, 122): ['DarkSalmon'],
    (238, 130, 238): ['Violet'],
    (238, 221, 130): ['LightGoldenrod'],
    (238, 232, 170): ['PaleGoldenrod'],
    (240, 128, 128): ['LightCoral'],
    (240, 230, 140): ['Khaki'],
    (240, 248, 255): ['AliceBlue'],
    (240, 255, 240): ['Honeydew'],
    (240, 255, 255): ['Azure'],
    (244, 164, 96): ['SandyBrown'],
    (245, 222, 179): ['Wheat'],
    (245, 245, 220): ['Beige'],
    (245, 245, 245): ['WhiteSmoke'],
    (245, 255, 250): ['MintCream'],
    (248, 248, 255): ['GhostWhite'],
    (250, 128, 114): ['Salmon'],
    (250, 235, 215): ['AntiqueWhite'],
    (250, 240, 230): ['Linen'],
    (250, 250, 210): ['LightGoldenrodYellow'],
    (253, 245, 230): ['OldLace'],
    (255, 0, 0): ['Red'],
    (255, 0, 255): ['Magenta', 'Fuchsia'],
    (255, 20, 147): ['DeepPink'],
    (255, 69, 0): ['OrangeRed'],
    (255, 99, 71): ['Tomato'],
    (255, 105, 180): ['HotPink'],
    (255, 127, 80): ['Coral'],
    (255, 140, 0): ['DarkOrange'],
    (255, 160, 122): ['LightSalmon'],
    (255, 165, 0): ['Orange'],
    (255, 182, 193): ['LightPink'],
    (255, 192, 203): ['Pink'],
    (255, 215, 0): ['Gold'],
    (255, 218, 185): ['PeachPuff'],
    (255, 222, 173): ['NavajoWhite'],
    (255, 228, 181): ['Moccasin'],
    (255, 228, 196): ['Bisque'],
    (255, 228, 225): ['MistyRose'],
    (255, 235, 205): ['BlanchedAlmond'],
    (255, 239, 213): ['PapayaWhip'],
    (255, 240, 245): ['LavenderBlush'],
    (255, 245, 238): ['Seashell'],
    (255, 248, 220): ['Cornsilk'],
    (255, 250, 205): ['LemonChiffon'],
    (255, 250, 240): ['FloralWhite'],
    (255, 250, 250): ['Snow'],
    (255, 255, 0): ['Yellow'],
    (255, 255, 224): ['LightYellow'],
    (255, 255, 240): ['Ivory'],
    (255, 255, 255): ['White']
}


def save_color_image(color_rgb_tuple_str, color_name):
    """Draw an image with specied color."""
    color_rgb_tuple = tuple([
        int(x) for x in
        color_rgb_tuple_str.replace('(', '').replace(')', '').split(',')])
    if Image:
        image = Image.new('RGB', (200, 200), color_rgb_tuple)
        draw = ImageDraw.Draw(image)
        image_file = os.path.join(IMAGE_DIR, '%s.png' % color_name)
        image.save(image_file)
    else:
        print('Please intall pillow to draw images with species names\n\n'
              '>>> pip install pillow')


def rgb_to_rgb_value(rgb_tuple_str):
    """
    Convert RGB to single RGB integer value.

    [Parameters]
        rgb_tuple_str: This kind of format: '(147,112,219)'

    [Return]
        rgb_value:  14381203
                    (
                        147
                        + (112 * 256)
                        + (219 * 256 * 256)
                    )

        RGB value= Red + (Green*256) + (Blue*256*256)
        (https://msdn.microsoft.com/en-us/library/dd355244.aspx)
    """
    r_value, g_value, b_value = [
        int(x) for x in
        rgb_tuple_str.replace('(', '').replace(')', '').split(',')]
    return r_value + (g_value * 256) + (b_value * 256 * 256)


def processing_raw_data(raw_data_file, data_file):
    """Processing raw data, apply [MIN_LIMIT, MAX_LIMIT] rule."""
    out_list = []
    with open(raw_data_file, 'r') as f_in:
        lines = [x.strip() for x in f_in.readlines() if x.strip()]

    for line in lines:
        number_list = [float(x) for x in line.split()]
        for i, number in enumerate(number_list):
            if number <= IGNORE_LIMIT:
                number_list[i] = 0
            elif IGNORE_LIMIT < number < MIN_LIMIT:
                number_list[i] = int(round(MIN_LIMIT))
            elif number > MAX_LIMIT:
                number_list[i] = int(round(MAX_LIMIT))
            else:
                number_list[i] = int(round(number))
        out_list.append(', '.join([str(x) for x in number_list]))

    with open(data_file, 'w') as f_out:
        f_out.write('\n'.join(out_list))


def generate_info_file(data_file):
    """Generate info_file."""
    out_list = []
    with open(data_file, 'r') as f_in:
        lines = [x.strip() for x in f_in.readlines() if x.strip()]

    for i, line in enumerate(lines):
        out_list.append('Hap_%d:\n\n' % (i+1))
        num_list = [int(x) for x in line.split(',')]
        num_sum = sum(num_list)
        for j, num in enumerate(num_list):
            if num:
                out_list.append(INFO_LINE_STYLE % (num, num_sum,
                                                   REGION_LISTS[j],
                                                   COLOR_LIST[j][1],
                                                   COLOR_LIST[j][0]))
        out_list.append('\n')

    with open('info_1.txt', 'w') as f_out:
        f_out.write('\n'.join(out_list))


class HandleFdi(object):
    """
    Modify fdi file to draw color.

    info_file was generated after HandleColorInfo()

    >>> hf = HandleFdi(fdi_file, info_file)
    >>> hf.parse_info_file()
    >>> hf.parse_fdi_file()
    >>> hf.write_to_file()
    """
    def __init__(self, fdi_file, info_file):
        self.info_file = info_file
        self.info_dict = {}
        self.fdi_file = fdi_file
        self.final_list = []

    def parse_info_file(self):
        """
        Parse infomation file and extract TAXON_PIE_FREQUENCY and RGB color.

        [Return]
            {
                'Hap_1': [['1 /  1:', 17919]],
                ...,
                'Hap_5': [
                             ['1 /  3:', 11394815],
                             ['1 /  3:', 2763429],
                             ['1 /  3:', 16776960]
                         ],
                ...
            }
        """
        temp_hap_name = ''
        exists_color_set = set()
        with open(self.info_file, 'r') as f_in:
            lines = [x.strip() for x in f_in.readlines() if x.strip()]

        for line in lines:
            print(line)
            if line.startswith("Hap_"):
                temp_hap_name = line.rstrip(':')
                self.info_dict[temp_hap_name] = []
            else:
                num_raw, name, rgb_tuple_str, color_name = \
                    [x.strip() for x in line.strip().split("|")
                     if x.strip()]

                # Save a image with name and color
                if color_name not in exists_color_set:
                    save_color_image(rgb_tuple_str, color_name)
                    exists_color_set.add(color_name)

                self.info_dict[temp_hap_name].append(
                    [num_raw, rgb_to_rgb_value(rgb_tuple_str)])

    def parse_fdi_file(self):
        """
        Parse fdi file and save modified lines to final list.
        """
        with open(self.fdi_file, 'r') as f_in:
            lines = f_in.readlines()

        for line in lines:
            if line.startswith("MIN_CIRC_RADIUS"):
                line = line.replace('4', MIN_CIRC_RADIUS)
                self.final_list.append(line)
            elif line.startswith("MAX_CIRC_RADIUS"):
                line = line.replace('50', MAX_CIRC_RADIUS)
                self.final_list.append(line)
            elif line.startswith("TAXON_NAME;H_"):
                # keep_part, throw_part
                keep_part, _ = line.split("TAXON_COLOR_PIE1")
                hap_num = line.split(";")[1].replace("H", "Hap").strip()
                # Infomation list
                # Example:
                #     [['8 /  8:', 16760576]],
                # or:
                #     [['7 / 27:', 11394815], ['5 / 27:', 2763429]]
                info_list = self.info_dict[hap_num]
                modified_line = ''
                modified_line += keep_part.rstrip("TAXON_COLOR_PIE1")
                for i, (num_raw, rgb_value) in enumerate(info_list):
                    frequency = num_raw.split("/")[0].strip()
                    modified_line += (
                        "TAXON_COLOR_PIE%d;%s;" % (i + 1, rgb_value) +
                        "TAXON_PIE_FREQUENCY%d;%s;" % (i + 1, frequency) +
                        "TAXON_STYLE_PIE%d;SOLID;" % (i + 1))
                modified_line += ("TAXON_LINE_WIDTH;1;" +
                                  "TAXON_LINE_COLOR;%s;" % BORDER_COLOR +
                                  "TAXON_LINE_STYLE;SOLID;" +
                                  "TAXON_ACTIVE;TRUE\n")
                self.final_list.append(modified_line)
            else:
                self.final_list.append(line)

    def write_to_file(self):
        """Write new fdi lines to file."""
        out_file = os.path.join(OUT_DIR, "new_%s" %
                                os.path.basename(self.fdi_file))
        with open(out_file, 'w') as f_out:
            f_out.write(''.join(self.final_list))


def generate_new_fdi():
    """Generate a new fdi with new proportions, new colors and new size limit.
    """
    fdi = HandleFdi(FDI_FILE, INFO_FILE)
    fdi.parse_info_file()
    fdi.parse_fdi_file()
    fdi.write_to_file()


def main():
    """Main func."""
    processing_raw_data(RAW_DATA_FILE, DATA_FILE)
    generate_info_file(DATA_FILE)
    generate_new_fdi()


if __name__ == '__main__':
    main()
