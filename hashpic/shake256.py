import sys, hashlib, os
from PIL import Image, ImageOps, ImageDraw
from .util import *
from .config import BLOCKSIZE


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
    round,
    bg_color,
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

    if variable_digest_length == 0xFF:
        hash += "ff"

    if svg:
        svg_mode(
            hash=hash,
            size=1200,
            digest_length=int(len(hash)/2),
            invert=invert,
            debug=debug,
            outputfile=outputfile,
            round=round,
            bg_color=bg_color,
        )

    if console:
        print_to_console(hash, invert, tile)

    width, height = 1200, 1200
    im = Image.new(mode="RGB", size=(width, height), color="#ffffff")

    colors = hash_to_color_codes(hash)
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
