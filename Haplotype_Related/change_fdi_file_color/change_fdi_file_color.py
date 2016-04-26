#!usr/bin/env python
# -*- coding: utf-8 -*-


"""Change color and size of fdi file.

Usage:

  1. put origin fdi files to a folder named "fdi_files"
  2. put txt files to a folder named "txt_files"
  3. put imap file to current folder
  4. run this script

"""

from __future__ import print_function, with_statement

import os
import sys
import random
try:
    from PIL import Image, ImageFont, ImageDraw
    import colorsys
except ImportError:
    Image, ImageFont, ImageDraw = None, None, None
    colorsys = None


MIN_CIRC_RADIUS = '10'
MAX_CIRC_RADIUS = '100'
BORDER_COLOR = '16777215'

# value, number, key, rgb(0,191,255), DeepSkyBlue
INFO_LINE_STYLE = "    %4d / %4d:\t|\t%18s\t|\t%15s\t|\t%18s"

EXISTS_COLOR_DICT = {}

# Input directory
FDI_DIR = os.path.abspath('./fdi_files')
TXT_DIR = os.path.abspath('./txt_files')

# Output directory
INFO_DIR = os.path.abspath('./info')
OUT_DIR = os.path.abspath('./output')
IMAGE_DIR = os.path.abspath('./images')

# Create dir if it does not exist
for each_dir in [FDI_DIR, TXT_DIR, INFO_DIR, OUT_DIR, IMAGE_DIR]:
    if not os.path.isdir(each_dir):
        os.mkdir(each_dir)

# Example input files
EXAM_FDI_FILE = '1.fdi'
EXAM_TXT_FILE = '1.txt'
EXAM_INFO_FILE = 'info_1.txt'
EXAM_OUTPUT_FILE = 'new_1.fdi'


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


def expand_num(num_str):
    """
    Expand number string to a list of numbers.

    [Parameters]
        num_str: A string which is this format: "1-14".

    [Example]
        num_list = expand_num("20-23")
        print(num_list)
        >>> [20, 21, 22, 23]
    """
    try:
        start, end = [int(x) for x in num_str.split('-')]
        if start > 0 and start <= end:
            return range(start, end + 1)
        else:
            print('Invalid parameter.\n    [Usage]: expand_num("2-4")\n')
    except BaseException as e:
        print('Invalid parameter.\n    [Usage]: expand_num("2-4")\n')
        print(e)
        sys.exit()


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


class ImapFile(object):
    """Handle imap file.

    Imap file:

        1 Black
        2 Black
        3 White
        4 Red
        5 Red
        6 ...
    """
    def __init__(self, imap_file):
        self.imap_file = imap_file
        self.lines = []
        self._prepare_data()

    def _prepare_data(self):
        with open(self.imap_file, 'r') as f_in:
            self.lines = [x.strip() for x in f_in.readlines() if x.strip()]

    @property
    def number_to_name_dict(self):
        """Get dictionary for number to name in imap file.

        Imap file:

            1 Black
            2 Black
            3 White
            4 Red
            5 Red

        get_relation_from_imap_file(imap_file):

            {'1': 'Black',
             '2': 'Black',
             '3': 'White',
             '4': 'Red',
             '5': 'Red'}
        """
        num_to_name_dict = {}
        for line in self.lines:
            num, name = line.split()
            num_to_name_dict[num] = name
        return num_to_name_dict

    @property
    def names(self):
        """Get all names from imap file."""
        name_set = set()
        for line in self.lines:
            _, name = line.split()
            name_set.add(name)

        return list(name_set)

    @property
    def blank_name_dict(self):
        """Generate a blank dict of names.
        Names:

            ['Black', 'White', 'Red']

        Blank name dict:

            {'Black': 0, 'White': 0, 'Red': 0}

        """
        name_dict = {}
        for name in self.names:
            name_dict[name] = 0

        return name_dict


class HandleColorInfo(object):
    """
    Handle txt file and write hap info and its color info into files.

    >>> hci = HandleColorInfo(txt_file, imap_file)
    >>> hci.write_to_file()

    Then we got a info_1.txt file in ./info directory.
    """
    def __init__(self, txt_file, imap_file):
        self.txt_file = txt_file
        self.imap_file = imap_file
        self.hap_info_list = []
        self._parse_content()

    def _parse_content(self):
        """
        Parse content from file and get useful part.
        """
        with open(self.txt_file, 'r') as f_in:
            useful_part = f_in.read().split('\n\n')[-2]

        for line in [x.strip() for x in useful_part.split('\n')]:
            hap_name, info = line.split(':')
            number, num_list_raw = info.split('  ')
            num_list = []
            for num in num_list_raw.replace('[', '').replace(']', '').split():
                if '-' in num:
                    num_list += expand_num(num)
                else:
                    num_list.append(int(num))

            self.hap_info_list.append([hap_name, int(number), num_list])

    @property
    def pretty_info(self):
        """
        Do pretty_info accroding to hap_info_list.

        Write outcome to a file baseed on input file.

            Hap_1:

                 5 /  5:      Black       rgb(0,191,255)       DeepSkyBlue

            Hap_2:

                 1 /  1:      Black       rgb(0,191,255)       DeepSkyBlue
            ...
        """
        final_list = []
        global EXISTS_COLOR_DICT
        imap = ImapFile(self.imap_file)
        number_to_name_dict = imap.number_to_name_dict

        for hap_name, number, num_list in self.hap_info_list:

            final_list.append("%s:\n" % hap_name)
            name_dict = imap.blank_name_dict

            for num in num_list:
                name_dict[number_to_name_dict[str(num)]] += 1

            for key, value in name_dict.iteritems():
                if value != 0:
                    if key not in EXISTS_COLOR_DICT:
                        random_rgb_tuple = random.choice(
                            RGB_TO_COLOR_NAMES.keys())
                        EXISTS_COLOR_DICT[key] = random_rgb_tuple
                    else:
                        random_rgb_tuple = EXISTS_COLOR_DICT[key]
                    color_name = RGB_TO_COLOR_NAMES[random_rgb_tuple]
                    final_list.append(INFO_LINE_STYLE % (
                        value, number, key,
                        ', '.join([str(x) for x in random_rgb_tuple]),
                        color_name[0]))
            final_list.append('\n')
        return final_list

    def write_to_file(self):
        """Write pretty info to file."""
        out_file = os.path.join(INFO_DIR, 'info_%s' %
                                os.path.basename(self.txt_file))
        with open(out_file, 'w') as f_out:
            f_out.write('\n'.join(self.pretty_info))
            print("--> Generated new info file: %s" %
                  os.path.basename(out_file))


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
            if line.startswith("Hap_"):
                temp_hap_name = line.rstrip(':')
                self.info_dict[temp_hap_name] = []
            else:
                print(line)
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
            print("  > Generated new fdi file:  %s" % os.path.basename(out_file))


def main():
    """Main func"""
    # Get imap_file
    imap_files = [x for x in os.listdir('.')
                  if x.lower().endswith('.imap.txt')]
    if len(imap_files) != 1:
        sys.exit('[ERROR] There should be one and only one *.imap.txt file')
    imap_file = imap_files[0]

    fdi_files = [os.path.join(FDI_DIR, x) for x in os.listdir(FDI_DIR)
                 if x.endswith('.fdi')]
    txt_files = [os.path.join(TXT_DIR, x) for x in os.listdir(TXT_DIR)
                 if x.endswith('.txt')]
    info_files = [os.path.join(INFO_DIR, 'info_%s' %
                               os.path.basename(x)) for x in txt_files]
    if len(fdi_files) != len(txt_files):
        sys.exit('[ERROR] Files in %s and in %s not match!' %
                 (FDI_DIR, TXT_DIR))

    for i, (fdi_file, txt_file) in enumerate(zip(fdi_files, txt_files)):
        # Generate info file
        hci = HandleColorInfo(txt_file, imap_file)
        hci.write_to_file()

        # Generate new fdi file
        fdi = HandleFdi(fdi_file, info_files[i])
        fdi.parse_info_file()
        fdi.parse_fdi_file()
        fdi.write_to_file()


if __name__ == '__main__':
    main()
