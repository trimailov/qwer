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

from math import floor
from PIL import Image


def find_closest(value):
    return 64 * floor(value/64)


def color_dither():
    new_img = Image.open('sonic.png')

    new_img = new_img.convert('RGB')
    pixel = new_img.load()

    x_lim, y_lim = new_img.size

    for y in range(1, y_lim):
        for x in range(1, x_lim):
            red_oldpixel, green_oldpixel, blue_oldpixel = pixel[x, y]

            red_newpixel = 255 * floor(red_oldpixel/128)
            green_newpixel = 255 * floor(green_oldpixel/128)
            blue_newpixel = 255 * floor(blue_oldpixel/128)

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


def bw_dither():
    img = Image.open('lena_bw.png')

    new_img = img.convert('L')
    pixel = new_img.load()

    x_lim, y_lim = img.size

    for y in range(0, y_lim):
        for x in range(0, x_lim):
            oldpixel = pixel[x, y]
            newpixel = 255 * floor(oldpixel/128)
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


if __name__ == "__main__":
    color_dither()
