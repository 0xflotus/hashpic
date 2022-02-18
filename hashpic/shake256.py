import sys, hashlib
from hashpic.util import *
from hashpic.config import BLOCKSIZE


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
    hexagon,
    stroke,
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
            digest_length=int(len(hash) / 2),
            invert=invert,
            debug=debug,
            outputfile=outputfile,
            round=round,
            hexagon=hexagon,
            with_stroke=stroke,
            bg_color=bg_color,
        )

    if console:
        print_to_console(hash, invert, tile)

    paint_png(hash=hash, size=1200, invert=invert, debug=debug, outputfile=outputfile)
