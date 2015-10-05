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

import sys


def apply_threshold(value):
    "Returns 0 or 255 depending where value is closer"
    return 255 * floor(value/128)


def color_dither(image_file):
    new_img = Image.open(image_file)

    new_img = new_img.convert('RGB')
    pixel = new_img.load()

    x_lim, y_lim = new_img.size

    for y in range(1, y_lim):
        for x in range(1, x_lim):
            red_oldpixel, green_oldpixel, blue_oldpixel = pixel[x, y]

            red_newpixel = apply_threshold(red_oldpixel)
            green_newpixel = apply_threshold(green_oldpixel)
            blue_newpixel = apply_threshold(blue_oldpixel)

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


def bw_dither(image_file):
    img = Image.open(image_file)

    new_img = img.convert('L')
    pixel = new_img.load()

    x_lim, y_lim = img.size

    for y in range(0, y_lim):
        for x in range(0, x_lim):
            oldpixel = pixel[x, y]
            newpixel = apply_threshold(oldpixel)
            pixel[x, y] = newpixel
            error = oldpixel - newpixel

            if x < x_lim - 1:
                pixel[x+1, y] += round(error * 7/16)

            if x > 1 and y < y_lim - 1:
                pixel[x-1, y+1] += round(error * 3/16)

            if y < y_lim - 1:
                pixel[x, y+1] += round(error * 5/16)

            if x < x_lim - 1 and y < y_lim - 1:
                pixel[x+1, y+1] += round(error * 1/16)

    new_img.show()


def main():
    parser = ArgumentParser(description="Image dithering in python")
    parser.add_argument("image", help="input image location")
    parser.add_argument("-o", help="output image location")
    args = parser.parse_args()

    if args.image:
        color_dither(args.image)
    elif: args.image and args.o:
        color_dither(args.image, save=True)
