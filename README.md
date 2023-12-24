# qwer

This script accomplishes [Floyd-Steinberg dithering](https://en.wikipedia.org/wiki/Floyd%E2%80%93Steinberg_dithering) in Python. Takes inputs as bitmap or png files. 

It is extremely useful for compression, especially the 1-bit ``--bw`` mode. In testing, this script in black and white mode was able to reduce 181x215 pixel image from 53.2KB to 4.89KB, albeit with all colour lost. Colour (default) mode reduced the image to 23.7KB.

## Usage

To use the script in colour, write as follows: ``python main.py lena.bmp -o lena.png``

If you wish to use the script in black and white: ``python main.py -o lena.png --bw``

## Creds

This script was originally created by [trimailov](https://github.com/trimailov). [lesageethan](https://github.com/lesageethan) added the 1-bit mode and transparency support.