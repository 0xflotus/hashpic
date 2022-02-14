import sys, hashlib, os
from PIL import Image, ImageOps
from .util import *
from .config import BLOCKSIZE
from tqdm import tqdm


def shake_256_mode(
    input,
    bypass,
    debug,
    console,
    tile,
    invert,
    digest_length,
    file,
    outputfile,
    svg,
    slow_mode=False,
):

    if not digest_length:
        sys.stderr.write("Please specify a --length\n")
        sys.exit(-1)

    variable_digest_length = int(digest_length)
    if variable_digest_length not in [1, 4, 9, 16, 25, 36, 64, 100, 144, 225, 255]:
        sys.stderr.write(
            "Sorry, only a length of one of [4, 9, 16, 25, 36, 64, 100, 144, 225, 255] is currently possible\n"
        )
        sys.exit(-1)

    if file:
        hash = file_to_hash(file, hashlib.shake_256(), variable_digest_length)
    elif not input:
        hash = (
            hashlib.shake_256(sys.stdin.read().encode()).hexdigest(
                variable_digest_length
            )
            if not bypass
            else sys.stdin.read().rstrip("\n").lower()
        )
    else:
        hash = (
            hashlib.shake_256(" ".join(input).encode()).hexdigest(
                variable_digest_length
            )
            if not bypass
            else input[0].lower()
        )

    validity_check(
        hash=hash,
        regex_str="^[a-f0-9]{%d}$" % (variable_digest_length * 2),
        name=f"SHAKE256-{variable_digest_length}",
    )

    if debug:
        debug_log(input=input, hash=hash, bypass=bypass)

    if svg:
        if variable_digest_length == 0xFF:
            hash += "ff"
            variable_digest_length += 1
        svg_mode(
            hash=hash,
            size=1200,
            digest_length=variable_digest_length,
            invert=invert,
            debug=debug,
            outputfile=outputfile,
        )

    if console:
        if variable_digest_length == 0xFF:
            hash += "ff"
        print_to_console(hash, invert, tile)

    width, height = 1200, 1200
    im = Image.new(mode="RGB", size=(width, height), color="#ffffff")
    pixels = im.load()

    colors = hash_to_color_codes(hash)

    if slow_mode:
        assert width == height, "width and height must be the same."
        assert width % 120 == 0, "size must be a multiple of 120"
        if variable_digest_length == 0xFF:
            colors.append(convert_term_to_rgb(0xFF))
            __paint(
                pixels, colors, size=width, digest_length=variable_digest_length + 1
            )
        else:
            __paint(pixels, colors, size=width, digest_length=variable_digest_length)
    else:
        if variable_digest_length == 0xFF:
            colors.append(convert_term_to_rgb(0xFF))
            __paint(
                pixels, colors, size=width, digest_length=variable_digest_length + 1
            )
        elif variable_digest_length == 0xE1:
            _225(pixels, colors, (width, height))
        elif variable_digest_length == 0x90:
            _144(pixels, colors, (width, height))
        elif variable_digest_length == 0x64:
            _100(pixels, colors, (width, height))
        elif variable_digest_length == 0x40:
            _64(pixels, colors, (width, height))
        elif variable_digest_length == 0x24:
            _36(pixels, colors, (width, height))
        elif variable_digest_length == 0x19:
            _25(pixels, colors, (width, height))
        elif variable_digest_length == 0x9:
            _9(pixels, colors, (width, height))
        elif variable_digest_length == 0x4:
            _4(pixels, colors, (width, height))
        elif variable_digest_length == 0x1:
            _1(pixels, colors, (width, height))
        else:
            _16(pixels, colors, (width, height))

    if invert:
        im = ImageOps.invert(im)

    if debug:
        im.show()

    im.save(os.getcwd() + "/" + outputfile)
    sys.exit(0)


def __paint(pixels, colors, size, digest_length):
    steps = int(size // (digest_length ** 0.5))
    store = [
        (y, y + steps, x, x + steps)
        for x in range(0, size, steps)
        for y in range(0, size, steps)
    ]

    for x in tqdm(range(size)):
        for y in range(size):
            for idx, (min_x, max_x, min_y, max_y) in enumerate(store):
                if min_x <= x < max_x and min_y <= y < max_y:
                    pixels[x, y] = colors[idx]


def _64(pixels, colors, dimension):
    (width, height) = dimension
    for x in tqdm(range(width)):
        for y in range(height):
            if x < 0x96 and y < 0x96:
                pixels[x, y] = colors[0]
            elif x < 0x12C and y < 0x96:
                pixels[x, y] = colors[1]
            elif x < 0x1C2 and y < 0x96:
                pixels[x, y] = colors[2]
            elif x < 0x258 and y < 0x96:
                pixels[x, y] = colors[3]
            elif x < 0x2EE and y < 0x96:
                pixels[x, y] = colors[4]
            elif x < 0x384 and y < 0x96:
                pixels[x, y] = colors[5]
            elif x < 0x41A and y < 0x96:
                pixels[x, y] = colors[6]
            elif x < 0x4B0 and y < 0x96:
                pixels[x, y] = colors[7]
            elif x < 0x96 and y < 0x12C:
                pixels[x, y] = colors[8]
            elif x < 0x12C and y < 0x12C:
                pixels[x, y] = colors[9]
            elif x < 0x1C2 and y < 0x12C:
                pixels[x, y] = colors[10]
            elif x < 0x258 and y < 0x12C:
                pixels[x, y] = colors[11]
            elif x < 0x2EE and y < 0x12C:
                pixels[x, y] = colors[12]
            elif x < 0x384 and y < 0x12C:
                pixels[x, y] = colors[13]
            elif x < 0x41A and y < 0x12C:
                pixels[x, y] = colors[14]
            elif x < 0x4B0 and y < 0x12C:
                pixels[x, y] = colors[15]
            elif x < 0x96 and y < 0x1C2:
                pixels[x, y] = colors[16]
            elif x < 0x12C and y < 0x1C2:
                pixels[x, y] = colors[17]
            elif x < 0x1C2 and y < 0x1C2:
                pixels[x, y] = colors[18]
            elif x < 0x258 and y < 0x1C2:
                pixels[x, y] = colors[19]
            elif x < 0x2EE and y < 0x1C2:
                pixels[x, y] = colors[20]
            elif x < 0x384 and y < 0x1C2:
                pixels[x, y] = colors[21]
            elif x < 0x41A and y < 0x1C2:
                pixels[x, y] = colors[22]
            elif x < 0x4B0 and y < 0x1C2:
                pixels[x, y] = colors[23]
            elif x < 0x96 and y < 0x258:
                pixels[x, y] = colors[24]
            elif x < 0x12C and y < 0x258:
                pixels[x, y] = colors[25]
            elif x < 0x1C2 and y < 0x258:
                pixels[x, y] = colors[26]
            elif x < 0x258 and y < 0x258:
                pixels[x, y] = colors[27]
            elif x < 0x2EE and y < 0x258:
                pixels[x, y] = colors[28]
            elif x < 0x384 and y < 0x258:
                pixels[x, y] = colors[29]
            elif x < 0x41A and y < 0x258:
                pixels[x, y] = colors[30]
            elif x < 0x4B0 and y < 0x258:
                pixels[x, y] = colors[31]
            elif x < 0x96 and y < 0x2EE:
                pixels[x, y] = colors[32]
            elif x < 0x12C and y < 0x2EE:
                pixels[x, y] = colors[33]
            elif x < 0x1C2 and y < 0x2EE:
                pixels[x, y] = colors[34]
            elif x < 0x258 and y < 0x2EE:
                pixels[x, y] = colors[35]
            elif x < 0x2EE and y < 0x2EE:
                pixels[x, y] = colors[36]
            elif x < 0x384 and y < 0x2EE:
                pixels[x, y] = colors[37]
            elif x < 0x41A and y < 0x2EE:
                pixels[x, y] = colors[38]
            elif x < 0x4B0 and y < 0x2EE:
                pixels[x, y] = colors[39]
            elif x < 0x96 and y < 0x384:
                pixels[x, y] = colors[40]
            elif x < 0x12C and y < 0x384:
                pixels[x, y] = colors[41]
            elif x < 0x1C2 and y < 0x384:
                pixels[x, y] = colors[42]
            elif x < 0x258 and y < 0x384:
                pixels[x, y] = colors[43]
            elif x < 0x2EE and y < 0x384:
                pixels[x, y] = colors[44]
            elif x < 0x384 and y < 0x384:
                pixels[x, y] = colors[45]
            elif x < 0x41A and y < 0x384:
                pixels[x, y] = colors[46]
            elif x < 0x4B0 and y < 0x384:
                pixels[x, y] = colors[47]
            elif x < 0x96 and y < 0x41A:
                pixels[x, y] = colors[48]
            elif x < 0x12C and y < 0x41A:
                pixels[x, y] = colors[49]
            elif x < 0x1C2 and y < 0x41A:
                pixels[x, y] = colors[50]
            elif x < 0x258 and y < 0x41A:
                pixels[x, y] = colors[51]
            elif x < 0x2EE and y < 0x41A:
                pixels[x, y] = colors[52]
            elif x < 0x384 and y < 0x41A:
                pixels[x, y] = colors[53]
            elif x < 0x41A and y < 0x41A:
                pixels[x, y] = colors[54]
            elif x < 0x4B0 and y < 0x41A:
                pixels[x, y] = colors[55]
            elif x < 0x96 and y < 0x4B0:
                pixels[x, y] = colors[56]
            elif x < 0x12C and y < 0x4B0:
                pixels[x, y] = colors[57]
            elif x < 0x1C2 and y < 0x4B0:
                pixels[x, y] = colors[58]
            elif x < 0x258 and y < 0x4B0:
                pixels[x, y] = colors[59]
            elif x < 0x2EE and y < 0x4B0:
                pixels[x, y] = colors[60]
            elif x < 0x384 and y < 0x4B0:
                pixels[x, y] = colors[61]
            elif x < 0x41A and y < 0x4B0:
                pixels[x, y] = colors[62]
            elif x < 0x4B0 and y < 0x4B0:
                pixels[x, y] = colors[63]
            else:
                pixels[x, y] = (0xFF, 0xFF, 0xFF)


def _1(pixels, colors, dimension):
    (width, height) = dimension
    for x in range(width):
        for y in range(height):
            pixels[x, y] = colors[0]


def _4(pixels, colors, dimension):
    (width, height) = dimension
    for x in range(width):
        for y in range(height):
            if x < 0x258 and y < 0x258:
                pixels[x, y] = colors[0]
            elif x < 0x4B0 and y < 0x258:
                pixels[x, y] = colors[1]
            elif x < 0x258 and y < 0x4B0:
                pixels[x, y] = colors[2]
            elif x < 0x4B0 and y < 0x4B0:
                pixels[x, y] = colors[3]
            else:
                pixels[x, y] = (0xFF, 0xFF, 0xFF)


def _9(pixels, colors, dimension):
    (width, height) = dimension
    for x in range(width):
        for y in range(height):
            if x < 0x190 and y < 0x190:
                pixels[x, y] = colors[0]
            elif x < 0x320 and y < 0x190:
                pixels[x, y] = colors[1]
            elif x < 0x4B0 and y < 0x190:
                pixels[x, y] = colors[2]
            elif x < 0x190 and y < 0x320:
                pixels[x, y] = colors[3]
            elif x < 0x320 and y < 0x320:
                pixels[x, y] = colors[4]
            elif x < 0x4B0 and y < 0x320:
                pixels[x, y] = colors[5]
            elif x < 0x190 and y < 0x4B0:
                pixels[x, y] = colors[6]
            elif x < 0x320 and y < 0x4B0:
                pixels[x, y] = colors[7]
            elif x < 0x4B0 and y < 0x4B0:
                pixels[x, y] = colors[8]
            else:
                pixels[x, y] = (0xFF, 0xFF, 0xFF)


def _16(pixels, colors, dimension):
    (width, height) = dimension
    for x in range(width):
        for y in range(height):
            if x < 0x12C and y < 0x12C:
                pixels[x, y] = colors[0]
            elif x < 0x258 and y < 0x12C:
                pixels[x, y] = colors[1]
            elif x < 0x384 and y < 0x12C:
                pixels[x, y] = colors[2]
            elif x < 0x4B0 and y < 0x12C:
                pixels[x, y] = colors[3]
            elif x < 0x12C and y < 0x258:
                pixels[x, y] = colors[4]
            elif x < 0x258 and y < 0x258:
                pixels[x, y] = colors[5]
            elif x < 0x384 and y < 0x258:
                pixels[x, y] = colors[6]
            elif x < 0x4B0 and y < 0x258:
                pixels[x, y] = colors[7]
            elif x < 0x12C and y < 0x384:
                pixels[x, y] = colors[8]
            elif x < 0x258 and y < 0x384:
                pixels[x, y] = colors[9]
            elif x < 0x384 and y < 0x384:
                pixels[x, y] = colors[10]
            elif x < 0x4B0 and y < 0x384:
                pixels[x, y] = colors[11]
            elif x < 0x12C and y < 0x4B0:
                pixels[x, y] = colors[12]
            elif x < 0x258 and y < 0x4B0:
                pixels[x, y] = colors[13]
            elif x < 0x384 and y < 0x4B0:
                pixels[x, y] = colors[14]
            elif x < 0x4B0 and y < 0x4B0:
                pixels[x, y] = colors[15]
            else:
                pixels[x, y] = (0xFF, 0xFF, 0xFF)


def _25(pixels, colors, dimension):
    (width, height) = dimension
    for x in range(width):
        for y in range(height):
            if x < 0xF0 and y < 0xF0:
                pixels[x, y] = colors[0]
            elif x < 0x1E0 and y < 0xF0:
                pixels[x, y] = colors[1]
            elif x < 0x2D0 and y < 0xF0:
                pixels[x, y] = colors[2]
            elif x < 0x3C0 and y < 0xF0:
                pixels[x, y] = colors[3]
            elif x < 0x4B0 and y < 0xF0:
                pixels[x, y] = colors[4]
            elif x < 0xF0 and y < 0x1E0:
                pixels[x, y] = colors[5]
            elif x < 0x1E0 and y < 0x1E0:
                pixels[x, y] = colors[6]
            elif x < 0x2D0 and y < 0x1E0:
                pixels[x, y] = colors[7]
            elif x < 0x3C0 and y < 0x1E0:
                pixels[x, y] = colors[8]
            elif x < 0x4B0 and y < 0x1E0:
                pixels[x, y] = colors[9]
            elif x < 0xF0 and y < 0x2D0:
                pixels[x, y] = colors[10]
            elif x < 0x1E0 and y < 0x2D0:
                pixels[x, y] = colors[11]
            elif x < 0x2D0 and y < 0x2D0:
                pixels[x, y] = colors[12]
            elif x < 0x3C0 and y < 0x2D0:
                pixels[x, y] = colors[13]
            elif x < 0x4B0 and y < 0x2D0:
                pixels[x, y] = colors[14]
            elif x < 0xF0 and y < 0x3C0:
                pixels[x, y] = colors[15]
            elif x < 0x1E0 and y < 0x3C0:
                pixels[x, y] = colors[16]
            elif x < 0x2D0 and y < 0x3C0:
                pixels[x, y] = colors[17]
            elif x < 0x3C0 and y < 0x3C0:
                pixels[x, y] = colors[18]
            elif x < 0x4B0 and y < 0x3C0:
                pixels[x, y] = colors[19]
            elif x < 0xF0 and y < 0x4B0:
                pixels[x, y] = colors[20]
            elif x < 0x1E0 and y < 0x4B0:
                pixels[x, y] = colors[21]
            elif x < 0x2D0 and y < 0x4B0:
                pixels[x, y] = colors[22]
            elif x < 0x3C0 and y < 0x4B0:
                pixels[x, y] = colors[23]
            elif x < 0x4B0 and y < 0x4B0:
                pixels[x, y] = colors[24]
            else:
                pixels[x, y] = (0xFF, 0xFF, 0xFF)


def _36(pixels, colors, dimension):
    (width, height) = dimension
    for x in range(width):
        for y in range(height):
            if x < 0xC8 and y < 0xC8:
                pixels[x, y] = colors[0]
            elif x < 0x190 and y < 0xC8:
                pixels[x, y] = colors[1]
            elif x < 0x258 and y < 0xC8:
                pixels[x, y] = colors[2]
            elif x < 0x320 and y < 0xC8:
                pixels[x, y] = colors[3]
            elif x < 0x3E8 and y < 0xC8:
                pixels[x, y] = colors[4]
            elif x < 0x4B0 and y < 0xC8:
                pixels[x, y] = colors[5]
            elif x < 0xC8 and y < 0x190:
                pixels[x, y] = colors[6]
            elif x < 0x190 and y < 0x190:
                pixels[x, y] = colors[7]
            elif x < 0x258 and y < 0x190:
                pixels[x, y] = colors[8]
            elif x < 0x320 and y < 0x190:
                pixels[x, y] = colors[9]
            elif x < 0x3E8 and y < 0x190:
                pixels[x, y] = colors[10]
            elif x < 0x4B0 and y < 0x190:
                pixels[x, y] = colors[11]
            elif x < 0xC8 and y < 0x258:
                pixels[x, y] = colors[12]
            elif x < 0x190 and y < 0x258:
                pixels[x, y] = colors[13]
            elif x < 0x258 and y < 0x258:
                pixels[x, y] = colors[14]
            elif x < 0x320 and y < 0x258:
                pixels[x, y] = colors[15]
            elif x < 0x3E8 and y < 0x258:
                pixels[x, y] = colors[16]
            elif x < 0x4B0 and y < 0x258:
                pixels[x, y] = colors[17]
            elif x < 0xC8 and y < 0x320:
                pixels[x, y] = colors[18]
            elif x < 0x190 and y < 0x320:
                pixels[x, y] = colors[19]
            elif x < 0x258 and y < 0x320:
                pixels[x, y] = colors[20]
            elif x < 0x320 and y < 0x320:
                pixels[x, y] = colors[21]
            elif x < 0x3E8 and y < 0x320:
                pixels[x, y] = colors[22]
            elif x < 0x4B0 and y < 0x320:
                pixels[x, y] = colors[23]
            elif x < 0xC8 and y < 0x3E8:
                pixels[x, y] = colors[24]
            elif x < 0x190 and y < 0x3E8:
                pixels[x, y] = colors[25]
            elif x < 0x258 and y < 0x3E8:
                pixels[x, y] = colors[26]
            elif x < 0x320 and y < 0x3E8:
                pixels[x, y] = colors[27]
            elif x < 0x3E8 and y < 0x3E8:
                pixels[x, y] = colors[28]
            elif x < 0x4B0 and y < 0x3E8:
                pixels[x, y] = colors[29]
            elif x < 0xC8 and y < 0x4B0:
                pixels[x, y] = colors[30]
            elif x < 0x190 and y < 0x4B0:
                pixels[x, y] = colors[31]
            elif x < 0x258 and y < 0x4B0:
                pixels[x, y] = colors[32]
            elif x < 0x320 and y < 0x4B0:
                pixels[x, y] = colors[33]
            elif x < 0x3E8 and y < 0x4B0:
                pixels[x, y] = colors[34]
            elif x < 0x4B0 and y < 0x4B0:
                pixels[x, y] = colors[35]
            else:
                pixels[x, y] = (0xFF, 0xFF, 0xFF)


def _100(pixels, colors, dimension):
    (width, height) = dimension
    for x in tqdm(range(width)):
        for y in range(height):
            if x < 0x78 and y < 0x78:
                pixels[x, y] = colors[0]
            elif x < 0xF0 and y < 0x78:
                pixels[x, y] = colors[1]
            elif x < 0x168 and y < 0x78:
                pixels[x, y] = colors[2]
            elif x < 0x1E0 and y < 0x78:
                pixels[x, y] = colors[3]
            elif x < 0x258 and y < 0x78:
                pixels[x, y] = colors[4]
            elif x < 0x2D0 and y < 0x78:
                pixels[x, y] = colors[5]
            elif x < 0x348 and y < 0x78:
                pixels[x, y] = colors[6]
            elif x < 0x3C0 and y < 0x78:
                pixels[x, y] = colors[7]
            elif x < 0x438 and y < 0x78:
                pixels[x, y] = colors[8]
            elif x < 0x4B0 and y < 0x78:
                pixels[x, y] = colors[9]
            elif x < 0x78 and y < 0xF0:
                pixels[x, y] = colors[10]
            elif x < 0xF0 and y < 0xF0:
                pixels[x, y] = colors[11]
            elif x < 0x168 and y < 0xF0:
                pixels[x, y] = colors[12]
            elif x < 0x1E0 and y < 0xF0:
                pixels[x, y] = colors[13]
            elif x < 0x258 and y < 0xF0:
                pixels[x, y] = colors[14]
            elif x < 0x2D0 and y < 0xF0:
                pixels[x, y] = colors[15]
            elif x < 0x348 and y < 0xF0:
                pixels[x, y] = colors[16]
            elif x < 0x3C0 and y < 0xF0:
                pixels[x, y] = colors[17]
            elif x < 0x438 and y < 0xF0:
                pixels[x, y] = colors[18]
            elif x < 0x4B0 and y < 0xF0:
                pixels[x, y] = colors[19]
            elif x < 0x78 and y < 0x168:
                pixels[x, y] = colors[20]
            elif x < 0xF0 and y < 0x168:
                pixels[x, y] = colors[21]
            elif x < 0x168 and y < 0x168:
                pixels[x, y] = colors[22]
            elif x < 0x1E0 and y < 0x168:
                pixels[x, y] = colors[23]
            elif x < 0x258 and y < 0x168:
                pixels[x, y] = colors[24]
            elif x < 0x2D0 and y < 0x168:
                pixels[x, y] = colors[25]
            elif x < 0x348 and y < 0x168:
                pixels[x, y] = colors[26]
            elif x < 0x3C0 and y < 0x168:
                pixels[x, y] = colors[27]
            elif x < 0x438 and y < 0x168:
                pixels[x, y] = colors[28]
            elif x < 0x4B0 and y < 0x168:
                pixels[x, y] = colors[29]
            elif x < 0x78 and y < 0x1E0:
                pixels[x, y] = colors[30]
            elif x < 0xF0 and y < 0x1E0:
                pixels[x, y] = colors[31]
            elif x < 0x168 and y < 0x1E0:
                pixels[x, y] = colors[32]
            elif x < 0x1E0 and y < 0x1E0:
                pixels[x, y] = colors[33]
            elif x < 0x258 and y < 0x1E0:
                pixels[x, y] = colors[34]
            elif x < 0x2D0 and y < 0x1E0:
                pixels[x, y] = colors[35]
            elif x < 0x348 and y < 0x1E0:
                pixels[x, y] = colors[36]
            elif x < 0x3C0 and y < 0x1E0:
                pixels[x, y] = colors[37]
            elif x < 0x438 and y < 0x1E0:
                pixels[x, y] = colors[38]
            elif x < 0x4B0 and y < 0x1E0:
                pixels[x, y] = colors[39]
            elif x < 0x78 and y < 0x258:
                pixels[x, y] = colors[40]
            elif x < 0xF0 and y < 0x258:
                pixels[x, y] = colors[41]
            elif x < 0x168 and y < 0x258:
                pixels[x, y] = colors[42]
            elif x < 0x1E0 and y < 0x258:
                pixels[x, y] = colors[43]
            elif x < 0x258 and y < 0x258:
                pixels[x, y] = colors[44]
            elif x < 0x2D0 and y < 0x258:
                pixels[x, y] = colors[45]
            elif x < 0x348 and y < 0x258:
                pixels[x, y] = colors[46]
            elif x < 0x3C0 and y < 0x258:
                pixels[x, y] = colors[47]
            elif x < 0x438 and y < 0x258:
                pixels[x, y] = colors[48]
            elif x < 0x4B0 and y < 0x258:
                pixels[x, y] = colors[49]
            elif x < 0x78 and y < 0x2D0:
                pixels[x, y] = colors[50]
            elif x < 0xF0 and y < 0x2D0:
                pixels[x, y] = colors[51]
            elif x < 0x168 and y < 0x2D0:
                pixels[x, y] = colors[52]
            elif x < 0x1E0 and y < 0x2D0:
                pixels[x, y] = colors[53]
            elif x < 0x258 and y < 0x2D0:
                pixels[x, y] = colors[54]
            elif x < 0x2D0 and y < 0x2D0:
                pixels[x, y] = colors[55]
            elif x < 0x348 and y < 0x2D0:
                pixels[x, y] = colors[56]
            elif x < 0x3C0 and y < 0x2D0:
                pixels[x, y] = colors[57]
            elif x < 0x438 and y < 0x2D0:
                pixels[x, y] = colors[58]
            elif x < 0x4B0 and y < 0x2D0:
                pixels[x, y] = colors[59]
            elif x < 0x78 and y < 0x348:
                pixels[x, y] = colors[60]
            elif x < 0xF0 and y < 0x348:
                pixels[x, y] = colors[61]
            elif x < 0x168 and y < 0x348:
                pixels[x, y] = colors[62]
            elif x < 0x1E0 and y < 0x348:
                pixels[x, y] = colors[63]
            elif x < 0x258 and y < 0x348:
                pixels[x, y] = colors[64]
            elif x < 0x2D0 and y < 0x348:
                pixels[x, y] = colors[65]
            elif x < 0x348 and y < 0x348:
                pixels[x, y] = colors[66]
            elif x < 0x3C0 and y < 0x348:
                pixels[x, y] = colors[67]
            elif x < 0x438 and y < 0x348:
                pixels[x, y] = colors[68]
            elif x < 0x4B0 and y < 0x348:
                pixels[x, y] = colors[69]
            elif x < 0x78 and y < 0x3C0:
                pixels[x, y] = colors[70]
            elif x < 0xF0 and y < 0x3C0:
                pixels[x, y] = colors[71]
            elif x < 0x168 and y < 0x3C0:
                pixels[x, y] = colors[72]
            elif x < 0x1E0 and y < 0x3C0:
                pixels[x, y] = colors[73]
            elif x < 0x258 and y < 0x3C0:
                pixels[x, y] = colors[74]
            elif x < 0x2D0 and y < 0x3C0:
                pixels[x, y] = colors[75]
            elif x < 0x348 and y < 0x3C0:
                pixels[x, y] = colors[76]
            elif x < 0x3C0 and y < 0x3C0:
                pixels[x, y] = colors[77]
            elif x < 0x438 and y < 0x3C0:
                pixels[x, y] = colors[78]
            elif x < 0x4B0 and y < 0x3C0:
                pixels[x, y] = colors[79]
            elif x < 0x78 and y < 0x438:
                pixels[x, y] = colors[80]
            elif x < 0xF0 and y < 0x438:
                pixels[x, y] = colors[81]
            elif x < 0x168 and y < 0x438:
                pixels[x, y] = colors[82]
            elif x < 0x1E0 and y < 0x438:
                pixels[x, y] = colors[83]
            elif x < 0x258 and y < 0x438:
                pixels[x, y] = colors[84]
            elif x < 0x2D0 and y < 0x438:
                pixels[x, y] = colors[85]
            elif x < 0x348 and y < 0x438:
                pixels[x, y] = colors[86]
            elif x < 0x3C0 and y < 0x438:
                pixels[x, y] = colors[87]
            elif x < 0x438 and y < 0x438:
                pixels[x, y] = colors[88]
            elif x < 0x4B0 and y < 0x438:
                pixels[x, y] = colors[89]
            elif x < 0x78 and y < 0x4B0:
                pixels[x, y] = colors[90]
            elif x < 0xF0 and y < 0x4B0:
                pixels[x, y] = colors[91]
            elif x < 0x168 and y < 0x4B0:
                pixels[x, y] = colors[92]
            elif x < 0x1E0 and y < 0x4B0:
                pixels[x, y] = colors[93]
            elif x < 0x258 and y < 0x4B0:
                pixels[x, y] = colors[94]
            elif x < 0x2D0 and y < 0x4B0:
                pixels[x, y] = colors[95]
            elif x < 0x348 and y < 0x4B0:
                pixels[x, y] = colors[96]
            elif x < 0x3C0 and y < 0x4B0:
                pixels[x, y] = colors[97]
            elif x < 0x438 and y < 0x4B0:
                pixels[x, y] = colors[98]
            elif x < 0x4B0 and y < 0x4B0:
                pixels[x, y] = colors[99]
            else:
                pixels[x, y] = (0xFF, 0xFF, 0xFF)


def _144(pixels, colors, dimension):
    (width, height) = dimension
    for x in tqdm(range(width)):
        for y in range(height):
            if x < 0x64 and y < 0x64:
                pixels[x, y] = colors[0]
            elif x < 0xC8 and y < 0x64:
                pixels[x, y] = colors[1]
            elif x < 0x12C and y < 0x64:
                pixels[x, y] = colors[2]
            elif x < 0x190 and y < 0x64:
                pixels[x, y] = colors[3]
            elif x < 0x1F4 and y < 0x64:
                pixels[x, y] = colors[4]
            elif x < 0x258 and y < 0x64:
                pixels[x, y] = colors[5]
            elif x < 0x2BC and y < 0x64:
                pixels[x, y] = colors[6]
            elif x < 0x320 and y < 0x64:
                pixels[x, y] = colors[7]
            elif x < 0x384 and y < 0x64:
                pixels[x, y] = colors[8]
            elif x < 0x3E8 and y < 0x64:
                pixels[x, y] = colors[9]
            elif x < 0x44C and y < 0x64:
                pixels[x, y] = colors[10]
            elif x < 0x4B0 and y < 0x64:
                pixels[x, y] = colors[11]
            elif x < 0x64 and y < 0xC8:
                pixels[x, y] = colors[12]
            elif x < 0xC8 and y < 0xC8:
                pixels[x, y] = colors[13]
            elif x < 0x12C and y < 0xC8:
                pixels[x, y] = colors[14]
            elif x < 0x190 and y < 0xC8:
                pixels[x, y] = colors[15]
            elif x < 0x1F4 and y < 0xC8:
                pixels[x, y] = colors[16]
            elif x < 0x258 and y < 0xC8:
                pixels[x, y] = colors[17]
            elif x < 0x2BC and y < 0xC8:
                pixels[x, y] = colors[18]
            elif x < 0x320 and y < 0xC8:
                pixels[x, y] = colors[19]
            elif x < 0x384 and y < 0xC8:
                pixels[x, y] = colors[20]
            elif x < 0x3E8 and y < 0xC8:
                pixels[x, y] = colors[21]
            elif x < 0x44C and y < 0xC8:
                pixels[x, y] = colors[22]
            elif x < 0x4B0 and y < 0xC8:
                pixels[x, y] = colors[23]
            elif x < 0x64 and y < 0x12C:
                pixels[x, y] = colors[24]
            elif x < 0xC8 and y < 0x12C:
                pixels[x, y] = colors[25]
            elif x < 0x12C and y < 0x12C:
                pixels[x, y] = colors[26]
            elif x < 0x190 and y < 0x12C:
                pixels[x, y] = colors[27]
            elif x < 0x1F4 and y < 0x12C:
                pixels[x, y] = colors[28]
            elif x < 0x258 and y < 0x12C:
                pixels[x, y] = colors[29]
            elif x < 0x2BC and y < 0x12C:
                pixels[x, y] = colors[30]
            elif x < 0x320 and y < 0x12C:
                pixels[x, y] = colors[31]
            elif x < 0x384 and y < 0x12C:
                pixels[x, y] = colors[32]
            elif x < 0x3E8 and y < 0x12C:
                pixels[x, y] = colors[33]
            elif x < 0x44C and y < 0x12C:
                pixels[x, y] = colors[34]
            elif x < 0x4B0 and y < 0x12C:
                pixels[x, y] = colors[35]
            elif x < 0x64 and y < 0x190:
                pixels[x, y] = colors[36]
            elif x < 0xC8 and y < 0x190:
                pixels[x, y] = colors[37]
            elif x < 0x12C and y < 0x190:
                pixels[x, y] = colors[38]
            elif x < 0x190 and y < 0x190:
                pixels[x, y] = colors[39]
            elif x < 0x1F4 and y < 0x190:
                pixels[x, y] = colors[40]
            elif x < 0x258 and y < 0x190:
                pixels[x, y] = colors[41]
            elif x < 0x2BC and y < 0x190:
                pixels[x, y] = colors[42]
            elif x < 0x320 and y < 0x190:
                pixels[x, y] = colors[43]
            elif x < 0x384 and y < 0x190:
                pixels[x, y] = colors[44]
            elif x < 0x3E8 and y < 0x190:
                pixels[x, y] = colors[45]
            elif x < 0x44C and y < 0x190:
                pixels[x, y] = colors[46]
            elif x < 0x4B0 and y < 0x190:
                pixels[x, y] = colors[47]
            elif x < 0x64 and y < 0x1F4:
                pixels[x, y] = colors[48]
            elif x < 0xC8 and y < 0x1F4:
                pixels[x, y] = colors[49]
            elif x < 0x12C and y < 0x1F4:
                pixels[x, y] = colors[50]
            elif x < 0x190 and y < 0x1F4:
                pixels[x, y] = colors[51]
            elif x < 0x1F4 and y < 0x1F4:
                pixels[x, y] = colors[52]
            elif x < 0x258 and y < 0x1F4:
                pixels[x, y] = colors[53]
            elif x < 0x2BC and y < 0x1F4:
                pixels[x, y] = colors[54]
            elif x < 0x320 and y < 0x1F4:
                pixels[x, y] = colors[55]
            elif x < 0x384 and y < 0x1F4:
                pixels[x, y] = colors[56]
            elif x < 0x3E8 and y < 0x1F4:
                pixels[x, y] = colors[57]
            elif x < 0x44C and y < 0x1F4:
                pixels[x, y] = colors[58]
            elif x < 0x4B0 and y < 0x1F4:
                pixels[x, y] = colors[59]
            elif x < 0x64 and y < 0x258:
                pixels[x, y] = colors[60]
            elif x < 0xC8 and y < 0x258:
                pixels[x, y] = colors[61]
            elif x < 0x12C and y < 0x258:
                pixels[x, y] = colors[62]
            elif x < 0x190 and y < 0x258:
                pixels[x, y] = colors[63]
            elif x < 0x1F4 and y < 0x258:
                pixels[x, y] = colors[64]
            elif x < 0x258 and y < 0x258:
                pixels[x, y] = colors[65]
            elif x < 0x2BC and y < 0x258:
                pixels[x, y] = colors[66]
            elif x < 0x320 and y < 0x258:
                pixels[x, y] = colors[67]
            elif x < 0x384 and y < 0x258:
                pixels[x, y] = colors[68]
            elif x < 0x3E8 and y < 0x258:
                pixels[x, y] = colors[69]
            elif x < 0x44C and y < 0x258:
                pixels[x, y] = colors[70]
            elif x < 0x4B0 and y < 0x258:
                pixels[x, y] = colors[71]
            elif x < 0x64 and y < 0x2BC:
                pixels[x, y] = colors[72]
            elif x < 0xC8 and y < 0x2BC:
                pixels[x, y] = colors[73]
            elif x < 0x12C and y < 0x2BC:
                pixels[x, y] = colors[74]
            elif x < 0x190 and y < 0x2BC:
                pixels[x, y] = colors[75]
            elif x < 0x1F4 and y < 0x2BC:
                pixels[x, y] = colors[76]
            elif x < 0x258 and y < 0x2BC:
                pixels[x, y] = colors[77]
            elif x < 0x2BC and y < 0x2BC:
                pixels[x, y] = colors[78]
            elif x < 0x320 and y < 0x2BC:
                pixels[x, y] = colors[79]
            elif x < 0x384 and y < 0x2BC:
                pixels[x, y] = colors[80]
            elif x < 0x3E8 and y < 0x2BC:
                pixels[x, y] = colors[81]
            elif x < 0x44C and y < 0x2BC:
                pixels[x, y] = colors[82]
            elif x < 0x4B0 and y < 0x2BC:
                pixels[x, y] = colors[83]
            elif x < 0x64 and y < 0x320:
                pixels[x, y] = colors[84]
            elif x < 0xC8 and y < 0x320:
                pixels[x, y] = colors[85]
            elif x < 0x12C and y < 0x320:
                pixels[x, y] = colors[86]
            elif x < 0x190 and y < 0x320:
                pixels[x, y] = colors[87]
            elif x < 0x1F4 and y < 0x320:
                pixels[x, y] = colors[88]
            elif x < 0x258 and y < 0x320:
                pixels[x, y] = colors[89]
            elif x < 0x2BC and y < 0x320:
                pixels[x, y] = colors[90]
            elif x < 0x320 and y < 0x320:
                pixels[x, y] = colors[91]
            elif x < 0x384 and y < 0x320:
                pixels[x, y] = colors[92]
            elif x < 0x3E8 and y < 0x320:
                pixels[x, y] = colors[93]
            elif x < 0x44C and y < 0x320:
                pixels[x, y] = colors[94]
            elif x < 0x4B0 and y < 0x320:
                pixels[x, y] = colors[95]
            elif x < 0x64 and y < 0x384:
                pixels[x, y] = colors[96]
            elif x < 0xC8 and y < 0x384:
                pixels[x, y] = colors[97]
            elif x < 0x12C and y < 0x384:
                pixels[x, y] = colors[98]
            elif x < 0x190 and y < 0x384:
                pixels[x, y] = colors[99]
            elif x < 0x1F4 and y < 0x384:
                pixels[x, y] = colors[100]
            elif x < 0x258 and y < 0x384:
                pixels[x, y] = colors[101]
            elif x < 0x2BC and y < 0x384:
                pixels[x, y] = colors[102]
            elif x < 0x320 and y < 0x384:
                pixels[x, y] = colors[103]
            elif x < 0x384 and y < 0x384:
                pixels[x, y] = colors[104]
            elif x < 0x3E8 and y < 0x384:
                pixels[x, y] = colors[105]
            elif x < 0x44C and y < 0x384:
                pixels[x, y] = colors[106]
            elif x < 0x4B0 and y < 0x384:
                pixels[x, y] = colors[107]
            elif x < 0x64 and y < 0x3E8:
                pixels[x, y] = colors[108]
            elif x < 0xC8 and y < 0x3E8:
                pixels[x, y] = colors[109]
            elif x < 0x12C and y < 0x3E8:
                pixels[x, y] = colors[110]
            elif x < 0x190 and y < 0x3E8:
                pixels[x, y] = colors[111]
            elif x < 0x1F4 and y < 0x3E8:
                pixels[x, y] = colors[112]
            elif x < 0x258 and y < 0x3E8:
                pixels[x, y] = colors[113]
            elif x < 0x2BC and y < 0x3E8:
                pixels[x, y] = colors[114]
            elif x < 0x320 and y < 0x3E8:
                pixels[x, y] = colors[115]
            elif x < 0x384 and y < 0x3E8:
                pixels[x, y] = colors[116]
            elif x < 0x3E8 and y < 0x3E8:
                pixels[x, y] = colors[117]
            elif x < 0x44C and y < 0x3E8:
                pixels[x, y] = colors[118]
            elif x < 0x4B0 and y < 0x3E8:
                pixels[x, y] = colors[119]
            elif x < 0x64 and y < 0x44C:
                pixels[x, y] = colors[120]
            elif x < 0xC8 and y < 0x44C:
                pixels[x, y] = colors[121]
            elif x < 0x12C and y < 0x44C:
                pixels[x, y] = colors[122]
            elif x < 0x190 and y < 0x44C:
                pixels[x, y] = colors[123]
            elif x < 0x1F4 and y < 0x44C:
                pixels[x, y] = colors[124]
            elif x < 0x258 and y < 0x44C:
                pixels[x, y] = colors[125]
            elif x < 0x2BC and y < 0x44C:
                pixels[x, y] = colors[126]
            elif x < 0x320 and y < 0x44C:
                pixels[x, y] = colors[127]
            elif x < 0x384 and y < 0x44C:
                pixels[x, y] = colors[128]
            elif x < 0x3E8 and y < 0x44C:
                pixels[x, y] = colors[129]
            elif x < 0x44C and y < 0x44C:
                pixels[x, y] = colors[130]
            elif x < 0x4B0 and y < 0x44C:
                pixels[x, y] = colors[131]
            elif x < 0x64 and y < 0x4B0:
                pixels[x, y] = colors[132]
            elif x < 0xC8 and y < 0x4B0:
                pixels[x, y] = colors[133]
            elif x < 0x12C and y < 0x4B0:
                pixels[x, y] = colors[134]
            elif x < 0x190 and y < 0x4B0:
                pixels[x, y] = colors[135]
            elif x < 0x1F4 and y < 0x4B0:
                pixels[x, y] = colors[136]
            elif x < 0x258 and y < 0x4B0:
                pixels[x, y] = colors[137]
            elif x < 0x2BC and y < 0x4B0:
                pixels[x, y] = colors[138]
            elif x < 0x320 and y < 0x4B0:
                pixels[x, y] = colors[139]
            elif x < 0x384 and y < 0x4B0:
                pixels[x, y] = colors[140]
            elif x < 0x3E8 and y < 0x4B0:
                pixels[x, y] = colors[141]
            elif x < 0x44C and y < 0x4B0:
                pixels[x, y] = colors[142]
            elif x < 0x4B0 and y < 0x4B0:
                pixels[x, y] = colors[143]
            else:
                pixels[x, y] = (0xFF, 0xFF, 0xFF)


def _225(pixels, colors, dimension):
    (width, height) = dimension
    for x in tqdm(range(width)):
        for y in range(height):
            if x < 0x50 and y < 0x50:
                pixels[x, y] = colors[0]
            elif x < 0xA0 and y < 0x50:
                pixels[x, y] = colors[1]
            elif x < 0xF0 and y < 0x50:
                pixels[x, y] = colors[2]
            elif x < 0x140 and y < 0x50:
                pixels[x, y] = colors[3]
            elif x < 0x190 and y < 0x50:
                pixels[x, y] = colors[4]
            elif x < 0x1E0 and y < 0x50:
                pixels[x, y] = colors[5]
            elif x < 0x230 and y < 0x50:
                pixels[x, y] = colors[6]
            elif x < 0x280 and y < 0x50:
                pixels[x, y] = colors[7]
            elif x < 0x2D0 and y < 0x50:
                pixels[x, y] = colors[8]
            elif x < 0x320 and y < 0x50:
                pixels[x, y] = colors[9]
            elif x < 0x370 and y < 0x50:
                pixels[x, y] = colors[10]
            elif x < 0x3C0 and y < 0x50:
                pixels[x, y] = colors[11]
            elif x < 0x410 and y < 0x50:
                pixels[x, y] = colors[12]
            elif x < 0x460 and y < 0x50:
                pixels[x, y] = colors[13]
            elif x < 0x4B0 and y < 0x50:
                pixels[x, y] = colors[14]
            elif x < 0x50 and y < 0xA0:
                pixels[x, y] = colors[15]
            elif x < 0xA0 and y < 0xA0:
                pixels[x, y] = colors[16]
            elif x < 0xF0 and y < 0xA0:
                pixels[x, y] = colors[17]
            elif x < 0x140 and y < 0xA0:
                pixels[x, y] = colors[18]
            elif x < 0x190 and y < 0xA0:
                pixels[x, y] = colors[19]
            elif x < 0x1E0 and y < 0xA0:
                pixels[x, y] = colors[20]
            elif x < 0x230 and y < 0xA0:
                pixels[x, y] = colors[21]
            elif x < 0x280 and y < 0xA0:
                pixels[x, y] = colors[22]
            elif x < 0x2D0 and y < 0xA0:
                pixels[x, y] = colors[23]
            elif x < 0x320 and y < 0xA0:
                pixels[x, y] = colors[24]
            elif x < 0x370 and y < 0xA0:
                pixels[x, y] = colors[25]
            elif x < 0x3C0 and y < 0xA0:
                pixels[x, y] = colors[26]
            elif x < 0x410 and y < 0xA0:
                pixels[x, y] = colors[27]
            elif x < 0x460 and y < 0xA0:
                pixels[x, y] = colors[28]
            elif x < 0x4B0 and y < 0xA0:
                pixels[x, y] = colors[29]
            elif x < 0x50 and y < 0xF0:
                pixels[x, y] = colors[30]
            elif x < 0xA0 and y < 0xF0:
                pixels[x, y] = colors[31]
            elif x < 0xF0 and y < 0xF0:
                pixels[x, y] = colors[32]
            elif x < 0x140 and y < 0xF0:
                pixels[x, y] = colors[33]
            elif x < 0x190 and y < 0xF0:
                pixels[x, y] = colors[34]
            elif x < 0x1E0 and y < 0xF0:
                pixels[x, y] = colors[35]
            elif x < 0x230 and y < 0xF0:
                pixels[x, y] = colors[36]
            elif x < 0x280 and y < 0xF0:
                pixels[x, y] = colors[37]
            elif x < 0x2D0 and y < 0xF0:
                pixels[x, y] = colors[38]
            elif x < 0x320 and y < 0xF0:
                pixels[x, y] = colors[39]
            elif x < 0x370 and y < 0xF0:
                pixels[x, y] = colors[40]
            elif x < 0x3C0 and y < 0xF0:
                pixels[x, y] = colors[41]
            elif x < 0x410 and y < 0xF0:
                pixels[x, y] = colors[42]
            elif x < 0x460 and y < 0xF0:
                pixels[x, y] = colors[43]
            elif x < 0x4B0 and y < 0xF0:
                pixels[x, y] = colors[44]
            elif x < 0x50 and y < 0x140:
                pixels[x, y] = colors[45]
            elif x < 0xA0 and y < 0x140:
                pixels[x, y] = colors[46]
            elif x < 0xF0 and y < 0x140:
                pixels[x, y] = colors[47]
            elif x < 0x140 and y < 0x140:
                pixels[x, y] = colors[48]
            elif x < 0x190 and y < 0x140:
                pixels[x, y] = colors[49]
            elif x < 0x1E0 and y < 0x140:
                pixels[x, y] = colors[50]
            elif x < 0x230 and y < 0x140:
                pixels[x, y] = colors[51]
            elif x < 0x280 and y < 0x140:
                pixels[x, y] = colors[52]
            elif x < 0x2D0 and y < 0x140:
                pixels[x, y] = colors[53]
            elif x < 0x320 and y < 0x140:
                pixels[x, y] = colors[54]
            elif x < 0x370 and y < 0x140:
                pixels[x, y] = colors[55]
            elif x < 0x3C0 and y < 0x140:
                pixels[x, y] = colors[56]
            elif x < 0x410 and y < 0x140:
                pixels[x, y] = colors[57]
            elif x < 0x460 and y < 0x140:
                pixels[x, y] = colors[58]
            elif x < 0x4B0 and y < 0x140:
                pixels[x, y] = colors[59]
            elif x < 0x50 and y < 0x190:
                pixels[x, y] = colors[60]
            elif x < 0xA0 and y < 0x190:
                pixels[x, y] = colors[61]
            elif x < 0xF0 and y < 0x190:
                pixels[x, y] = colors[62]
            elif x < 0x140 and y < 0x190:
                pixels[x, y] = colors[63]
            elif x < 0x190 and y < 0x190:
                pixels[x, y] = colors[64]
            elif x < 0x1E0 and y < 0x190:
                pixels[x, y] = colors[65]
            elif x < 0x230 and y < 0x190:
                pixels[x, y] = colors[66]
            elif x < 0x280 and y < 0x190:
                pixels[x, y] = colors[67]
            elif x < 0x2D0 and y < 0x190:
                pixels[x, y] = colors[68]
            elif x < 0x320 and y < 0x190:
                pixels[x, y] = colors[69]
            elif x < 0x370 and y < 0x190:
                pixels[x, y] = colors[70]
            elif x < 0x3C0 and y < 0x190:
                pixels[x, y] = colors[71]
            elif x < 0x410 and y < 0x190:
                pixels[x, y] = colors[72]
            elif x < 0x460 and y < 0x190:
                pixels[x, y] = colors[73]
            elif x < 0x4B0 and y < 0x190:
                pixels[x, y] = colors[74]
            elif x < 0x50 and y < 0x1E0:
                pixels[x, y] = colors[75]
            elif x < 0xA0 and y < 0x1E0:
                pixels[x, y] = colors[76]
            elif x < 0xF0 and y < 0x1E0:
                pixels[x, y] = colors[77]
            elif x < 0x140 and y < 0x1E0:
                pixels[x, y] = colors[78]
            elif x < 0x190 and y < 0x1E0:
                pixels[x, y] = colors[79]
            elif x < 0x1E0 and y < 0x1E0:
                pixels[x, y] = colors[80]
            elif x < 0x230 and y < 0x1E0:
                pixels[x, y] = colors[81]
            elif x < 0x280 and y < 0x1E0:
                pixels[x, y] = colors[82]
            elif x < 0x2D0 and y < 0x1E0:
                pixels[x, y] = colors[83]
            elif x < 0x320 and y < 0x1E0:
                pixels[x, y] = colors[84]
            elif x < 0x370 and y < 0x1E0:
                pixels[x, y] = colors[85]
            elif x < 0x3C0 and y < 0x1E0:
                pixels[x, y] = colors[86]
            elif x < 0x410 and y < 0x1E0:
                pixels[x, y] = colors[87]
            elif x < 0x460 and y < 0x1E0:
                pixels[x, y] = colors[88]
            elif x < 0x4B0 and y < 0x1E0:
                pixels[x, y] = colors[89]
            elif x < 0x50 and y < 0x230:
                pixels[x, y] = colors[90]
            elif x < 0xA0 and y < 0x230:
                pixels[x, y] = colors[91]
            elif x < 0xF0 and y < 0x230:
                pixels[x, y] = colors[92]
            elif x < 0x140 and y < 0x230:
                pixels[x, y] = colors[93]
            elif x < 0x190 and y < 0x230:
                pixels[x, y] = colors[94]
            elif x < 0x1E0 and y < 0x230:
                pixels[x, y] = colors[95]
            elif x < 0x230 and y < 0x230:
                pixels[x, y] = colors[96]
            elif x < 0x280 and y < 0x230:
                pixels[x, y] = colors[97]
            elif x < 0x2D0 and y < 0x230:
                pixels[x, y] = colors[98]
            elif x < 0x320 and y < 0x230:
                pixels[x, y] = colors[99]
            elif x < 0x370 and y < 0x230:
                pixels[x, y] = colors[100]
            elif x < 0x3C0 and y < 0x230:
                pixels[x, y] = colors[101]
            elif x < 0x410 and y < 0x230:
                pixels[x, y] = colors[102]
            elif x < 0x460 and y < 0x230:
                pixels[x, y] = colors[103]
            elif x < 0x4B0 and y < 0x230:
                pixels[x, y] = colors[104]
            elif x < 0x50 and y < 0x280:
                pixels[x, y] = colors[105]
            elif x < 0xA0 and y < 0x280:
                pixels[x, y] = colors[106]
            elif x < 0xF0 and y < 0x280:
                pixels[x, y] = colors[107]
            elif x < 0x140 and y < 0x280:
                pixels[x, y] = colors[108]
            elif x < 0x190 and y < 0x280:
                pixels[x, y] = colors[109]
            elif x < 0x1E0 and y < 0x280:
                pixels[x, y] = colors[110]
            elif x < 0x230 and y < 0x280:
                pixels[x, y] = colors[111]
            elif x < 0x280 and y < 0x280:
                pixels[x, y] = colors[112]
            elif x < 0x2D0 and y < 0x280:
                pixels[x, y] = colors[113]
            elif x < 0x320 and y < 0x280:
                pixels[x, y] = colors[114]
            elif x < 0x370 and y < 0x280:
                pixels[x, y] = colors[115]
            elif x < 0x3C0 and y < 0x280:
                pixels[x, y] = colors[116]
            elif x < 0x410 and y < 0x280:
                pixels[x, y] = colors[117]
            elif x < 0x460 and y < 0x280:
                pixels[x, y] = colors[118]
            elif x < 0x4B0 and y < 0x280:
                pixels[x, y] = colors[119]
            elif x < 0x50 and y < 0x2D0:
                pixels[x, y] = colors[120]
            elif x < 0xA0 and y < 0x2D0:
                pixels[x, y] = colors[121]
            elif x < 0xF0 and y < 0x2D0:
                pixels[x, y] = colors[122]
            elif x < 0x140 and y < 0x2D0:
                pixels[x, y] = colors[123]
            elif x < 0x190 and y < 0x2D0:
                pixels[x, y] = colors[124]
            elif x < 0x1E0 and y < 0x2D0:
                pixels[x, y] = colors[125]
            elif x < 0x230 and y < 0x2D0:
                pixels[x, y] = colors[126]
            elif x < 0x280 and y < 0x2D0:
                pixels[x, y] = colors[127]
            elif x < 0x2D0 and y < 0x2D0:
                pixels[x, y] = colors[128]
            elif x < 0x320 and y < 0x2D0:
                pixels[x, y] = colors[129]
            elif x < 0x370 and y < 0x2D0:
                pixels[x, y] = colors[130]
            elif x < 0x3C0 and y < 0x2D0:
                pixels[x, y] = colors[131]
            elif x < 0x410 and y < 0x2D0:
                pixels[x, y] = colors[132]
            elif x < 0x460 and y < 0x2D0:
                pixels[x, y] = colors[133]
            elif x < 0x4B0 and y < 0x2D0:
                pixels[x, y] = colors[134]
            elif x < 0x50 and y < 0x320:
                pixels[x, y] = colors[135]
            elif x < 0xA0 and y < 0x320:
                pixels[x, y] = colors[136]
            elif x < 0xF0 and y < 0x320:
                pixels[x, y] = colors[137]
            elif x < 0x140 and y < 0x320:
                pixels[x, y] = colors[138]
            elif x < 0x190 and y < 0x320:
                pixels[x, y] = colors[139]
            elif x < 0x1E0 and y < 0x320:
                pixels[x, y] = colors[140]
            elif x < 0x230 and y < 0x320:
                pixels[x, y] = colors[141]
            elif x < 0x280 and y < 0x320:
                pixels[x, y] = colors[142]
            elif x < 0x2D0 and y < 0x320:
                pixels[x, y] = colors[143]
            elif x < 0x320 and y < 0x320:
                pixels[x, y] = colors[144]
            elif x < 0x370 and y < 0x320:
                pixels[x, y] = colors[145]
            elif x < 0x3C0 and y < 0x320:
                pixels[x, y] = colors[146]
            elif x < 0x410 and y < 0x320:
                pixels[x, y] = colors[147]
            elif x < 0x460 and y < 0x320:
                pixels[x, y] = colors[148]
            elif x < 0x4B0 and y < 0x320:
                pixels[x, y] = colors[149]
            elif x < 0x50 and y < 0x370:
                pixels[x, y] = colors[150]
            elif x < 0xA0 and y < 0x370:
                pixels[x, y] = colors[151]
            elif x < 0xF0 and y < 0x370:
                pixels[x, y] = colors[152]
            elif x < 0x140 and y < 0x370:
                pixels[x, y] = colors[153]
            elif x < 0x190 and y < 0x370:
                pixels[x, y] = colors[154]
            elif x < 0x1E0 and y < 0x370:
                pixels[x, y] = colors[155]
            elif x < 0x230 and y < 0x370:
                pixels[x, y] = colors[156]
            elif x < 0x280 and y < 0x370:
                pixels[x, y] = colors[157]
            elif x < 0x2D0 and y < 0x370:
                pixels[x, y] = colors[158]
            elif x < 0x320 and y < 0x370:
                pixels[x, y] = colors[159]
            elif x < 0x370 and y < 0x370:
                pixels[x, y] = colors[160]
            elif x < 0x3C0 and y < 0x370:
                pixels[x, y] = colors[161]
            elif x < 0x410 and y < 0x370:
                pixels[x, y] = colors[162]
            elif x < 0x460 and y < 0x370:
                pixels[x, y] = colors[163]
            elif x < 0x4B0 and y < 0x370:
                pixels[x, y] = colors[164]
            elif x < 0x50 and y < 0x3C0:
                pixels[x, y] = colors[165]
            elif x < 0xA0 and y < 0x3C0:
                pixels[x, y] = colors[166]
            elif x < 0xF0 and y < 0x3C0:
                pixels[x, y] = colors[167]
            elif x < 0x140 and y < 0x3C0:
                pixels[x, y] = colors[168]
            elif x < 0x190 and y < 0x3C0:
                pixels[x, y] = colors[169]
            elif x < 0x1E0 and y < 0x3C0:
                pixels[x, y] = colors[170]
            elif x < 0x230 and y < 0x3C0:
                pixels[x, y] = colors[171]
            elif x < 0x280 and y < 0x3C0:
                pixels[x, y] = colors[172]
            elif x < 0x2D0 and y < 0x3C0:
                pixels[x, y] = colors[173]
            elif x < 0x320 and y < 0x3C0:
                pixels[x, y] = colors[174]
            elif x < 0x370 and y < 0x3C0:
                pixels[x, y] = colors[175]
            elif x < 0x3C0 and y < 0x3C0:
                pixels[x, y] = colors[176]
            elif x < 0x410 and y < 0x3C0:
                pixels[x, y] = colors[177]
            elif x < 0x460 and y < 0x3C0:
                pixels[x, y] = colors[178]
            elif x < 0x4B0 and y < 0x3C0:
                pixels[x, y] = colors[179]
            elif x < 0x50 and y < 0x410:
                pixels[x, y] = colors[180]
            elif x < 0xA0 and y < 0x410:
                pixels[x, y] = colors[181]
            elif x < 0xF0 and y < 0x410:
                pixels[x, y] = colors[182]
            elif x < 0x140 and y < 0x410:
                pixels[x, y] = colors[183]
            elif x < 0x190 and y < 0x410:
                pixels[x, y] = colors[184]
            elif x < 0x1E0 and y < 0x410:
                pixels[x, y] = colors[185]
            elif x < 0x230 and y < 0x410:
                pixels[x, y] = colors[186]
            elif x < 0x280 and y < 0x410:
                pixels[x, y] = colors[187]
            elif x < 0x2D0 and y < 0x410:
                pixels[x, y] = colors[188]
            elif x < 0x320 and y < 0x410:
                pixels[x, y] = colors[189]
            elif x < 0x370 and y < 0x410:
                pixels[x, y] = colors[190]
            elif x < 0x3C0 and y < 0x410:
                pixels[x, y] = colors[191]
            elif x < 0x410 and y < 0x410:
                pixels[x, y] = colors[192]
            elif x < 0x460 and y < 0x410:
                pixels[x, y] = colors[193]
            elif x < 0x4B0 and y < 0x410:
                pixels[x, y] = colors[194]
            elif x < 0x50 and y < 0x460:
                pixels[x, y] = colors[195]
            elif x < 0xA0 and y < 0x460:
                pixels[x, y] = colors[196]
            elif x < 0xF0 and y < 0x460:
                pixels[x, y] = colors[197]
            elif x < 0x140 and y < 0x460:
                pixels[x, y] = colors[198]
            elif x < 0x190 and y < 0x460:
                pixels[x, y] = colors[199]
            elif x < 0x1E0 and y < 0x460:
                pixels[x, y] = colors[200]
            elif x < 0x230 and y < 0x460:
                pixels[x, y] = colors[201]
            elif x < 0x280 and y < 0x460:
                pixels[x, y] = colors[202]
            elif x < 0x2D0 and y < 0x460:
                pixels[x, y] = colors[203]
            elif x < 0x320 and y < 0x460:
                pixels[x, y] = colors[204]
            elif x < 0x370 and y < 0x460:
                pixels[x, y] = colors[205]
            elif x < 0x3C0 and y < 0x460:
                pixels[x, y] = colors[206]
            elif x < 0x410 and y < 0x460:
                pixels[x, y] = colors[207]
            elif x < 0x460 and y < 0x460:
                pixels[x, y] = colors[208]
            elif x < 0x4B0 and y < 0x460:
                pixels[x, y] = colors[209]
            elif x < 0x50 and y < 0x4B0:
                pixels[x, y] = colors[210]
            elif x < 0xA0 and y < 0x4B0:
                pixels[x, y] = colors[211]
            elif x < 0xF0 and y < 0x4B0:
                pixels[x, y] = colors[212]
            elif x < 0x140 and y < 0x4B0:
                pixels[x, y] = colors[213]
            elif x < 0x190 and y < 0x4B0:
                pixels[x, y] = colors[214]
            elif x < 0x1E0 and y < 0x4B0:
                pixels[x, y] = colors[215]
            elif x < 0x230 and y < 0x4B0:
                pixels[x, y] = colors[216]
            elif x < 0x280 and y < 0x4B0:
                pixels[x, y] = colors[217]
            elif x < 0x2D0 and y < 0x4B0:
                pixels[x, y] = colors[218]
            elif x < 0x320 and y < 0x4B0:
                pixels[x, y] = colors[219]
            elif x < 0x370 and y < 0x4B0:
                pixels[x, y] = colors[220]
            elif x < 0x3C0 and y < 0x4B0:
                pixels[x, y] = colors[221]
            elif x < 0x410 and y < 0x4B0:
                pixels[x, y] = colors[222]
            elif x < 0x460 and y < 0x4B0:
                pixels[x, y] = colors[223]
            elif x < 0x4B0 and y < 0x4B0:
                pixels[x, y] = colors[224]
            else:
                pixels[x, y] = (0xFF, 0xFF, 0xFF)
