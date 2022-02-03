import sys, re, hashlib, os, math
from PIL import Image, ImageOps
from .util import *


def shake_256_mode(input, bypass, debug, console, invert, digest_length):

    if not digest_length:
        sys.stderr.write("Please specify a --length\n")
        sys.exit(-1)

    if int(digest_length) not in [16, 25, 36, 64]:
        sys.stderr.write(
            "Sorry, only a length of one of [16, 25, 36, 64] is currently possible\n"
        )
        sys.exit(-1)

    variable_digest_length = int(digest_length)

    if not input:
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

    regex_dict = {
        16: r"^[a-f0-9]{32}$",
        25: r"^[a-f0-9]{50}$",
        36: r"^[a-f0-9]{72}$",
        64: r"^[a-f0-9]{128}$",
    }

    regex_str = regex_dict[variable_digest_length]
    pattern = re.compile(regex_str)
    match = pattern.match(hash)
    if not match:
        sys.stderr.write(
            f"{hash} is not a valid SHAKE256 hash with digest length of {variable_digest_length}\n"
        )
        sys.exit(-1)

    if debug:
        sys.stdout.write(
            f'hashpic: "{input}" will be following hash: {hash}\n'
            if not bypass
            else f"hashpic: directly given hash: {input}\n"
        )

    if console:
        chunks = chunk_it(chunk_it(hash), int(math.sqrt(variable_digest_length)))

        for i in chunks:
            for j in i:
                sys.stdout.write(
                    f"\033[38;5;{0xff - int(j, 16) if invert else int(j, 16)}m{j}\u001b[0m"
                )
            sys.stdout.write("\n")
        sys.exit(0)

    colors = []
    for i in chunk_it(hash):
        colors.append(convert_term_to_rgb(int(i, 16)))

    width = 1200
    height = 1200

    im = Image.new(mode="RGB", size=(width, height), color="#ffffff")
    pixels = im.load()

    if variable_digest_length == 0x40:
        _64(pixels, colors, (width, height))
    elif variable_digest_length == 0x24:
        _36(pixels, colors, (width, height))
    elif variable_digest_length == 0x19:
        _25(pixels, colors, (width, height))
    else:
        _16(pixels, colors, (width, height))

    if invert:
        im = ImageOps.invert(im)

    if debug:
        im.show()

    im.save(os.getcwd() + "/output.png")

    sys.exit(0)


def _64(pixels, colors, dimension):
    (width, height) = dimension
    for x in range(width):
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
            if x < 0xc8 and y < 0xc8:
                pixels[x, y] = colors[0]
            elif x < 0x190 and y < 0xc8:
                pixels[x, y] = colors[1]
            elif x < 0x258 and y < 0xc8:
                pixels[x, y] = colors[2]
            elif x < 0x320 and y < 0xc8:
                pixels[x, y] = colors[3]
            elif x < 0x3e8 and y < 0xc8:
                pixels[x, y] = colors[4]
            elif x < 0x4b0 and y < 0xc8:
                pixels[x, y] = colors[5]
            elif x < 0xc8 and y < 0x190:
                pixels[x, y] = colors[6]
            elif x < 0x190 and y < 0x190:
                pixels[x, y] = colors[7]
            elif x < 0x258 and y < 0x190:
                pixels[x, y] = colors[8]
            elif x < 0x320 and y < 0x190:
                pixels[x, y] = colors[9]
            elif x < 0x3e8 and y < 0x190:
                pixels[x, y] = colors[10]
            elif x < 0x4b0 and y < 0x190:
                pixels[x, y] = colors[11]
            elif x < 0xc8 and y < 0x258:
                pixels[x, y] = colors[12]
            elif x < 0x190 and y < 0x258:
                pixels[x, y] = colors[13]
            elif x < 0x258 and y < 0x258:
                pixels[x, y] = colors[14]
            elif x < 0x320 and y < 0x258:
                pixels[x, y] = colors[15]
            elif x < 0x3e8 and y < 0x258:
                pixels[x, y] = colors[16]
            elif x < 0x4b0 and y < 0x258:
                pixels[x, y] = colors[17]
            elif x < 0xc8 and y < 0x320:
                pixels[x, y] = colors[18]
            elif x < 0x190 and y < 0x320:
                pixels[x, y] = colors[19]
            elif x < 0x258 and y < 0x320:
                pixels[x, y] = colors[20]
            elif x < 0x320 and y < 0x320:
                pixels[x, y] = colors[21]
            elif x < 0x3e8 and y < 0x320:
                pixels[x, y] = colors[22]
            elif x < 0x4b0 and y < 0x320:
                pixels[x, y] = colors[23]
            elif x < 0xc8 and y < 0x3e8:
                pixels[x, y] = colors[24]
            elif x < 0x190 and y < 0x3e8:
                pixels[x, y] = colors[25]
            elif x < 0x258 and y < 0x3e8:
                pixels[x, y] = colors[26]
            elif x < 0x320 and y < 0x3e8:
                pixels[x, y] = colors[27]
            elif x < 0x3e8 and y < 0x3e8:
                pixels[x, y] = colors[28]
            elif x < 0x4b0 and y < 0x3e8:
                pixels[x, y] = colors[29]
            elif x < 0xc8 and y < 0x4b0:
                pixels[x, y] = colors[30]
            elif x < 0x190 and y < 0x4b0:
                pixels[x, y] = colors[31]
            elif x < 0x258 and y < 0x4b0:
                pixels[x, y] = colors[32]
            elif x < 0x320 and y < 0x4b0:
                pixels[x, y] = colors[33]
            elif x < 0x3e8 and y < 0x4b0:
                pixels[x, y] = colors[34]
            elif x < 0x4b0 and y < 0x4b0:
                pixels[x, y] = colors[35]
            else:
                pixels[x, y] = (0xFF, 0xFF, 0xFF)