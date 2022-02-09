import sys, re, hashlib, os
from PIL import Image, ImageOps
from .util import *


def sha3_512_mode(input, bypass, debug, console, tile, invert, file, outputfile, svg):

    if file:
        BLOCKSIZE = 0x1000
        hasher = hashlib.sha3_512()
        with open(file, "rb") as tfile:
            buffer = tfile.read(BLOCKSIZE)
            while len(buffer) > 0:
                hasher.update(buffer)
                buffer = tfile.read(BLOCKSIZE)
        hash = hasher.hexdigest().lower()
    elif not input:
        hash = (
            hashlib.sha3_512(sys.stdin.read().encode()).hexdigest()
            if not bypass
            else sys.stdin.read().rstrip("\n").lower()
        )
    else:
        hash = (
            hashlib.sha3_512(" ".join(input).encode()).hexdigest()
            if not bypass
            else input[0].lower()
        )

    pattern = re.compile(r"^[a-f0-9]{128}$")
    match = pattern.match(hash)
    if not match:
        sys.stderr.write(f"{hash} is not a valid SHA3-512 hash\n")
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
                map(lambda cc: (0xFF - cc[0], 0xFF - cc[1], 0xFF - cc[2]), color_codes)
            )
        SVG = paint_svg(0x400, 0x40, color_codes)

        if debug:
            sys.stdout.write(SVG)
            sys.exit(0)

        filename = os.getcwd() + "/" + outputfile
        f = open(filename, "w")
        f.write(SVG)
        f.close()
        sys.exit(0)

    if console:
        chunks = chunk_it(chunk_it(hash), 8)

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
            if x < 0x80 and y < 0x80:
                pixels[x, y] = colors[0]
            elif x < 0x100 and y < 0x80:
                pixels[x, y] = colors[1]
            elif x < 0x180 and y < 0x80:
                pixels[x, y] = colors[2]
            elif x < 0x200 and y < 0x80:
                pixels[x, y] = colors[3]
            elif x < 0x280 and y < 0x80:
                pixels[x, y] = colors[4]
            elif x < 0x300 and y < 0x80:
                pixels[x, y] = colors[5]
            elif x < 0x380 and y < 0x80:
                pixels[x, y] = colors[6]
            elif x < 0x400 and y < 0x80:
                pixels[x, y] = colors[7]
            elif x < 0x80 and y < 0x100:
                pixels[x, y] = colors[8]
            elif x < 0x100 and y < 0x100:
                pixels[x, y] = colors[9]
            elif x < 0x180 and y < 0x100:
                pixels[x, y] = colors[10]
            elif x < 0x200 and y < 0x100:
                pixels[x, y] = colors[11]
            elif x < 0x280 and y < 0x100:
                pixels[x, y] = colors[12]
            elif x < 0x300 and y < 0x100:
                pixels[x, y] = colors[13]
            elif x < 0x380 and y < 0x100:
                pixels[x, y] = colors[14]
            elif x < 0x400 and y < 0x100:
                pixels[x, y] = colors[15]
            elif x < 0x80 and y < 0x180:
                pixels[x, y] = colors[16]
            elif x < 0x100 and y < 0x180:
                pixels[x, y] = colors[17]
            elif x < 0x180 and y < 0x180:
                pixels[x, y] = colors[18]
            elif x < 0x200 and y < 0x180:
                pixels[x, y] = colors[19]
            elif x < 0x280 and y < 0x180:
                pixels[x, y] = colors[20]
            elif x < 0x300 and y < 0x180:
                pixels[x, y] = colors[21]
            elif x < 0x380 and y < 0x180:
                pixels[x, y] = colors[22]
            elif x < 0x400 and y < 0x180:
                pixels[x, y] = colors[23]
            elif x < 0x80 and y < 0x200:
                pixels[x, y] = colors[24]
            elif x < 0x100 and y < 0x200:
                pixels[x, y] = colors[25]
            elif x < 0x180 and y < 0x200:
                pixels[x, y] = colors[26]
            elif x < 0x200 and y < 0x200:
                pixels[x, y] = colors[27]
            elif x < 0x280 and y < 0x200:
                pixels[x, y] = colors[28]
            elif x < 0x300 and y < 0x200:
                pixels[x, y] = colors[29]
            elif x < 0x380 and y < 0x200:
                pixels[x, y] = colors[30]
            elif x < 0x400 and y < 0x200:
                pixels[x, y] = colors[31]
            elif x < 0x80 and y < 0x280:
                pixels[x, y] = colors[32]
            elif x < 0x100 and y < 0x280:
                pixels[x, y] = colors[33]
            elif x < 0x180 and y < 0x280:
                pixels[x, y] = colors[34]
            elif x < 0x200 and y < 0x280:
                pixels[x, y] = colors[35]
            elif x < 0x280 and y < 0x280:
                pixels[x, y] = colors[36]
            elif x < 0x300 and y < 0x280:
                pixels[x, y] = colors[37]
            elif x < 0x380 and y < 0x280:
                pixels[x, y] = colors[38]
            elif x < 0x400 and y < 0x280:
                pixels[x, y] = colors[39]
            elif x < 0x80 and y < 0x300:
                pixels[x, y] = colors[40]
            elif x < 0x100 and y < 0x300:
                pixels[x, y] = colors[41]
            elif x < 0x180 and y < 0x300:
                pixels[x, y] = colors[42]
            elif x < 0x200 and y < 0x300:
                pixels[x, y] = colors[43]
            elif x < 0x280 and y < 0x300:
                pixels[x, y] = colors[44]
            elif x < 0x300 and y < 0x300:
                pixels[x, y] = colors[45]
            elif x < 0x380 and y < 0x300:
                pixels[x, y] = colors[46]
            elif x < 0x400 and y < 0x300:
                pixels[x, y] = colors[47]
            elif x < 0x80 and y < 0x380:
                pixels[x, y] = colors[48]
            elif x < 0x100 and y < 0x380:
                pixels[x, y] = colors[49]
            elif x < 0x180 and y < 0x380:
                pixels[x, y] = colors[50]
            elif x < 0x200 and y < 0x380:
                pixels[x, y] = colors[51]
            elif x < 0x280 and y < 0x380:
                pixels[x, y] = colors[52]
            elif x < 0x300 and y < 0x380:
                pixels[x, y] = colors[53]
            elif x < 0x380 and y < 0x380:
                pixels[x, y] = colors[54]
            elif x < 0x400 and y < 0x380:
                pixels[x, y] = colors[55]
            elif x < 0x80 and y < 0x400:
                pixels[x, y] = colors[56]
            elif x < 0x100 and y < 0x400:
                pixels[x, y] = colors[57]
            elif x < 0x180 and y < 0x400:
                pixels[x, y] = colors[58]
            elif x < 0x200 and y < 0x400:
                pixels[x, y] = colors[59]
            elif x < 0x280 and y < 0x400:
                pixels[x, y] = colors[60]
            elif x < 0x300 and y < 0x400:
                pixels[x, y] = colors[61]
            elif x < 0x380 and y < 0x400:
                pixels[x, y] = colors[62]
            elif x < 0x400 and y < 0x400:
                pixels[x, y] = colors[63]
            else:
                pixels[x, y] = (0xFF, 0xFF, 0xFF)

    if invert:
        im = ImageOps.invert(im)

    if debug:
        im.show()

    im.save(os.getcwd() + "/" + outputfile)

    sys.exit(0)
