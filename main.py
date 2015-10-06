#!/usr/bin/python3

# https://en.wikipedia.org/wiki/Floyd–Steinberg_dithering
#
# Pseudocode:
#
# for each y from top to bottom
#    for each x from left to right
#       oldpixel  := pixel[x][y]
#       newpixel  := find_closest_palette_color(oldpixel)
#       pixel[x][y]  := newpixel
#       quant_error  := oldpixel - newpixel
#       pixel[x+1][y  ] := pixel[x+1][y  ] + quant_error * 7/16
#       pixel[x-1][y+1] := pixel[x-1][y+1] + quant_error * 3/16
#       pixel[x  ][y+1] := pixel[x  ][y+1] + quant_error * 5/16
#       pixel[x+1][y+1] := pixel[x+1][y+1] + quant_error * 1/16
#
# find_closest_palette_color(oldpixel) = floor(oldpixel / 256)

from argparse import ArgumentParser
from math import floor
from PIL import Image

import os


class Dither():
    def __init__(self, path, algorithm=None, output=None):
        self.path = self.get_path(path)
        self.algorithm = algorithm
        self.output = output
        self.func = self.get_func(self.algorithm)
        self.func(self.path)

    def get_path(self, path):
        """Get whole path of an image

        If path does not start with '/', then try to open image from pwd
        If path starts with '/', then open image of given path
        """
        if path.startswith('/') and not path.startswith('~/'):
            return os.getcwd() + '/' + path
        else:
            return path

    def get_func(self, algorithm):
        "Get dithering function to run"
        return self.floyd_steinberg_dither

    def apply_threshold(self, value):
        "Returns 0 or 255 depending where value is closer"
        return 255 * floor(value/128)

    def floyd_steinberg_dither(self, image_file):
        new_img = Image.open(image_file)

        new_img = new_img.convert('RGB')
        pixel = new_img.load()

        x_lim, y_lim = new_img.size

        for y in range(1, y_lim):
            for x in range(1, x_lim):
                red_oldpixel, green_oldpixel, blue_oldpixel = pixel[x, y]

                red_newpixel = self.apply_threshold(red_oldpixel)
                green_newpixel = self.apply_threshold(green_oldpixel)
                blue_newpixel = self.apply_threshold(blue_oldpixel)

                pixel[x, y] = red_newpixel, green_newpixel, blue_newpixel

                red_error = red_oldpixel - red_newpixel
                blue_error = blue_oldpixel - blue_newpixel
                green_error = green_oldpixel - green_newpixel

                if x < x_lim - 1:
                    red = pixel[x+1, y][0] + round(red_error * 7/16)
                    green = pixel[x+1, y][1] + round(green_error * 7/16)
                    blue = pixel[x+1, y][2] + round(blue_error * 7/16)

                    pixel[x+1, y] = (red, green, blue)

                if x > 1 and y < y_lim - 1:
                    red = pixel[x-1, y+1][0] + round(red_error * 3/16)
                    green = pixel[x-1, y+1][1] + round(green_error * 3/16)
                    blue = pixel[x-1, y+1][2] + round(blue_error * 3/16)

                    pixel[x-1, y+1] = (red, green, blue)

                if y < y_lim - 1:
                    red = pixel[x, y+1][0] + round(red_error * 5/16)
                    green = pixel[x, y+1][1] + round(green_error * 5/16)
                    blue = pixel[x, y+1][2] + round(blue_error * 5/16)

                    pixel[x, y+1] = (red, green, blue)

                if x < x_lim - 1 and y < y_lim - 1:
                    red = pixel[x+1, y+1][0] + round(red_error * 1/16)
                    green = pixel[x+1, y+1][1] + round(green_error * 1/16)
                    blue = pixel[x+1, y+1][2] + round(blue_error * 1/16)

                    pixel[x+1, y+1] = (red, green, blue)

        new_img.show()


def main():
    parser = ArgumentParser(description="Image dithering in python")
    parser.add_argument("image_path", help="input image location")
    parser.add_argument("-o", help="output image location")
    args = parser.parse_args()

    if args.image_path:
        Dither(args.image_path)
    elif args.image_path and args.o:
        Dither(args.image)
