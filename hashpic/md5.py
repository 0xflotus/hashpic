from PIL import Image, ImageOps
import os
import hashlib
import sys
import re
from .util import *


def md5_mode(input, bypass, debug, console, tile, invert, file, outputfile, svg):

    if file:
        BLOCKSIZE = 0x1000
        hasher = hashlib.md5()
        with open(file, "rb") as tfile:
            buffer = tfile.read(BLOCKSIZE)
            while len(buffer) > 0:
                hasher.update(buffer)
                buffer = tfile.read(BLOCKSIZE)
        hash = hasher.hexdigest().lower()
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

    pattern = re.compile(r"^[a-f0-9]{32}$")
    match = pattern.match(hash)
    if not match:
        sys.stderr.write(f"{hash} is not a valid MD5 hash\n")
        sys.exit(-1)

    if debug:
        sys.stdout.write(
            f'hashpic: "{input}" will be following hash: {hash}\n'
            if not bypass
            else f"hashpic: directly given hash: {input}\n"
        )

    if svg:
        color_codes = hash_to_color_codes(hash)
        if invert:
            color_codes = list(
                map(lambda cc: (cc[0] ^ 0xFF, cc[1] ^ 0xFF, cc[2] ^ 0xFF), color_codes)
            )
        SVG = paint_svg(0x400, 0x10, color_codes)

        if debug:
            sys.stdout.write(SVG)
            sys.exit(0)

        filename = os.getcwd() + "/" + outputfile
        f = open(filename, "w")
        f.write(SVG)
        f.close()
        sys.exit(0)

    if console:
        chunks = chunk_it(chunk_it(hash), 4)

        for i in chunks:
            for j in i:
                sys.stdout.write(
                    f"\033[38;5;{0xff - int(j, 16) if invert else int(j, 16)}m{j if not tile else '▮'}\u001b[0m"
                )
            sys.stdout.write("\n")
        sys.exit(0)

    colors = []
    for i in chunk_it(hash):
        colors.append(convert_term_to_rgb(int(i, 16)))

    width = 1024
    height = 1024

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
