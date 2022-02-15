import sys, hashlib, os
from PIL import Image, ImageOps, ImageDraw
from .util import *

def sha3_512_mode(
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
        hash = file_to_hash(file, hashlib.sha3_512())
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

    validity_check(hash=hash, regex_str=r"^[a-f0-9]{128}$", name="SHA3-512")

    if debug:
        debug_log(input=input, hash=hash, bypass=bypass)

    if svg:
        svg_mode(
            hash=hash,
            size=0x400,
            digest_length=0x40,
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
    m_size = int((len(hash) // 2) ** 0.5)
    steps = int(width // m_size)
    store = [
        (i, steps * (x + 1), i + steps, steps * x)
        for x in range(m_size)
        for i in range(0, width, steps)
    ]

    for idx, elem in enumerate(store):
        draw.rectangle(elem, fill=colors[idx])

    if invert:
        im = ImageOps.invert(im)

    if debug:
        im.show()

    im.save(os.getcwd() + "/" + outputfile)
    sys.exit(0)
