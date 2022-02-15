from PIL import Image, ImageOps
import os, hashlib, sys
from .util import *


def md5_mode(input, bypass, debug, console, tile, invert, file, outputfile, svg, round):

    if file:
        hash = file_to_hash(file, hashlib.md5())
    elif not input:
        hash = (
            hashlib.md5(sys.stdin.read().encode()).hexdigest()
            if not bypass
            else sys.stdin.read().rstrip("\n").lower()
        )
    else:
        hash = (
            hashlib.md5(" ".join(input).encode()).hexdigest()
            if not bypass
            else input[0].lower()
        )

    validity_check(hash=hash, regex_str=r"^[a-f0-9]{32}$", name="MD5")

    if debug:
        debug_log(input=input, hash=hash, bypass=bypass)

    if svg:
        svg_mode(
            hash=hash,
            size=0x400,
            digest_length=0x10,
            invert=invert,
            debug=debug,
            outputfile=outputfile,
            round=round,
        )

    if console:
        print_to_console(hash, invert, tile)

    colors = hash_to_color_codes(hash)

    width, height = 1024, 1024

    im = Image.new(mode="RGB", size=(width, height), color="#ffffff")
    pixels = im.load()
    for x in range(width):
        for y in range(height):
            if x < 0x100 and y < 0x100:
                pixels[x, y] = colors[0]
            elif x < 0x200 and y < 0x100:
                pixels[x, y] = colors[1]
            elif x < 0x300 and y < 0x100:
                pixels[x, y] = colors[2]
            elif x < 0x400 and y < 0x100:
                pixels[x, y] = colors[3]
            elif x < 0x100 and y < 0x200:
                pixels[x, y] = colors[4]
            elif x < 0x200 and y < 0x200:
                pixels[x, y] = colors[5]
            elif x < 0x300 and y < 0x200:
                pixels[x, y] = colors[6]
            elif x < 0x400 and y < 0x200:
                pixels[x, y] = colors[7]
            elif x < 0x100 and y < 0x300:
                pixels[x, y] = colors[8]
            elif x < 0x200 and y < 0x300:
                pixels[x, y] = colors[9]
            elif x < 0x300 and y < 0x300:
                pixels[x, y] = colors[10]
            elif x < 0x400 and y < 0x300:
                pixels[x, y] = colors[11]
            elif x < 0x100 and y < 0x400:
                pixels[x, y] = colors[12]
            elif x < 0x200 and y < 0x400:
                pixels[x, y] = colors[13]
            elif x < 0x300 and y < 0x400:
                pixels[x, y] = colors[14]
            elif x < 0x400 and y < 0x400:
                pixels[x, y] = colors[15]
            else:
                pixels[x, y] = (0xFF, 0xFF, 0xFF)

    if invert:
        im = ImageOps.invert(im)

    if debug:
        im.show()

    im.save(os.getcwd() + "/" + outputfile)
    sys.exit(0)
