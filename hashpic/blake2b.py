import sys, hashlib
from hashpic.util import *


def blake2b_mode(
    input,
    bypass,
    debug,
    console,
    tile,
    invert,
    file,
    outputfile,
    svg,
    hexagon,
    stroke,
    round,
    bg_color,
):
    if file:
        hash = file_to_hash(file, hashlib.blake2b())
    elif not input:
        hash = (
            hashlib.blake2b(sys.stdin.read().encode()).hexdigest()
            if not bypass
            else sys.stdin.read().rstrip("\n").lower()
        )
    else:
        hash = (
            hashlib.blake2b(" ".join(input).encode()).hexdigest()
            if not bypass
            else input[0].lower()
        )

    validity_check(hash=hash, regex_str=r"^[a-f0-9]{128}$", name="BLAKE2b")

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
            hexagon=hexagon,
            with_stroke=stroke,
            bg_color=bg_color,
        )

    if console:
        print_to_console(hash, invert, tile)

    paint_png(hash=hash, size=0x400, invert=invert, debug=debug, outputfile=outputfile)
