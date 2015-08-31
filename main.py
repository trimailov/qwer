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


img = Image.open('lena.bmp')
img_data = img.getdata()

new_img = Image.new('RGB', img.size, 'black')
new_pixel = new_img.load()

x_lim, y_lim = img.size

pixel = img_data.getpixel

for y in range(1, y_lim):
    for x in range(1, x_lim):
        red_oldpixel, green_oldpixel, blue_oldpixel = pixel((x, y))

        red_newpixel = find_closest(red_oldpixel)
        green_newpixel = find_closest(green_oldpixel)
        blue_newpixel = find_closest(blue_oldpixel)

        red_error = red_oldpixel - red_newpixel
        blue_error = blue_oldpixel - blue_newpixel
        green_error = green_oldpixel - green_newpixel

        if x < 511:
            red = pixel((x+1, y))[0] + floor(red_error * 7/16)
            green = pixel((x+1, y))[1] + floor(green_error * 7/16)
            blue = pixel((x+1, y))[2] + floor(blue_error * 7/16)

            new_pixel[x, y-1] = (red, green, blue)

        if x > 1 and y < 511:
            red = pixel((x-1, y+1))[0] + floor(red_error * 3/16)
            green = pixel((x-1, y+1))[1] + floor(green_error * 3/16)
            blue = pixel((x-1, y+1))[2] + floor(blue_error * 3/16)

            new_pixel[x-2, y] = (red, green, blue)

        if y < 511:
            red = pixel((x, y+1))[0] + floor(red_error * 5/16)
            green = pixel((x, y+1))[1] + floor(green_error * 5/16)
            blue = pixel((x, y+1))[2] + floor(blue_error * 5/16)

            new_pixel[x-1, y] = (red, green, blue)

        if x < 511 and y < 511:
            red = pixel((x+1, y+1))[0] + floor(red_error * 1/16)
            green = pixel((x+1, y+1))[1] + floor(green_error * 1/16)
            blue = pixel((x+1, y+1))[2] + floor(blue_error * 1/16)

            new_pixel[x, y] = (red, green, blue)

new_img.show()
