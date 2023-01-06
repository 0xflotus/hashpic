import sys
from hashpic.util import *
from MD6 import MD6

def md6_mode(
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
        raise NotImplementedError('Not implemented for MD6')
    elif not input:
        md6 = MD6(size=0x200)
        md6_hash = md6(sys.stdin.read().encode())
        print(str(md6_hash))
        hash = (
            str(md6_hash)
            if not bypass
            else sys.stdin.read().rstrip("\n").lower()
        )
    else:
        md6 = MD6(size=0x200)
        md6_hash = md6(input[0])
        print(str(md6_hash))
        hash = (
            str(md6_hash)
            if not bypass
            else input[0].lower()
        )

    validity_check(hash=hash, regex_str=r"^[a-f0-9]{128}$", name="MD6")

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
    