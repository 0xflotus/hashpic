from PIL import Image, ImageOps, ImageDraw
import os, hashlib, sys
from .util import *


def md5_mode(
    input,
    bypass,
    debug,
    console,
    tile,
    invert,
    file,
    outputfile,
    svg,
    round,
    bg_color,
):

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
            bg_color=bg_color,
        )

    if console:
        print_to_console(hash, invert, tile)

    colors = hash_to_color_codes(hash)

    width, height = 1024, 1024

    im = Image.new(mode="RGB", size=(width, height), color="#ffffff")
    draw = ImageDraw.Draw(im)

    draw.rectangle((0x0, 0x100, 0x100, 0x0), fill=colors[0])
    draw.rectangle((0x100, 0x100, 0x200, 0x0), fill=colors[1])
    draw.rectangle((0x200, 0x100, 0x300, 0x0), fill=colors[2])
    draw.rectangle((0x300, 0x100, 0x400, 0x0), fill=colors[3])
    
    draw.rectangle((0x0, 0x200, 0x100, 0x100), fill=colors[4])
    draw.rectangle((0x100, 0x200, 0x200, 0x100), fill=colors[5])
    draw.rectangle((0x200, 0x200, 0x300, 0x100), fill=colors[6])
    draw.rectangle((0x300, 0x200, 0x400, 0x100), fill=colors[7])

    draw.rectangle((0x0, 0x300, 0x100, 0x200), fill=colors[8])
    draw.rectangle((0x100, 0x300, 0x200, 0x200), fill=colors[9])
    draw.rectangle((0x200, 0x300, 0x300, 0x200), fill=colors[10])
    draw.rectangle((0x300, 0x300, 0x400, 0x200), fill=colors[11])

    draw.rectangle((0x0, 0x400, 0x100, 0x300), fill=colors[12])
    draw.rectangle((0x100, 0x400, 0x200, 0x300), fill=colors[13])
    draw.rectangle((0x200, 0x400, 0x300, 0x300), fill=colors[14])
    draw.rectangle((0x300, 0x400, 0x400, 0x300), fill=colors[15])

    if invert:
        im = ImageOps.invert(im)

    if debug:
        im.show()

    im.save(os.getcwd() + "/" + outputfile)
    sys.exit(0)
