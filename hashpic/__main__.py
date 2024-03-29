import argparse
from hashpic import __version__
from hashpic.md5 import *
from hashpic.sha512 import *
from hashpic.shake256 import *
from hashpic.blake2b import *
from hashpic.sha3 import *
from hashpic.md6 import *


def main():
    parser = argparse.ArgumentParser(
        prog="hashpic",
        description="Create an image from a MD5, SHA512, SHA3-512, Blake2b or Shake256 hash",
    )
    parser.add_argument(
        "-v", action="version", version=f"{__version__}", help="Version"
    )
    parser.add_argument("input", nargs="*", action="store", help="Input string to hash")
    parser.add_argument("-d", action="store_true", help="debug mode")
    parser.add_argument("-i", action="store_true", help="invert the image")
    parser.add_argument("--bypass", action="store_true", help="give a hash directly")
    parser.add_argument("-c", action="store_true", help="console mode")
    parser.add_argument("--tile", action="store_true")
    parser.add_argument("--sha512", action="store_true")
    parser.add_argument("--shake256", action="store_true")
    parser.add_argument("--sha3", action="store_true")
    parser.add_argument("--blake2b", action="store_true")
    parser.add_argument("--md6", action="store_true")
    parser.add_argument("--length", action="store")
    parser.add_argument("--file", action="store")
    parser.add_argument("--svg", action="store_true")
    parser.add_argument("--hexagon", action="store_true")
    parser.add_argument("--stroke", action="store_true")
    parser.add_argument("--round", action="store_true")
    parser.add_argument("--background", action="store")
    parser.add_argument("-o", action="store")
    args = parser.parse_args()

    outputfile = args.o or "output"
    outputfile += ".svg" if args.svg else ".png"

    if args.sha512:
        sha_512_mode(
            input=args.input,
            bypass=args.bypass,
            debug=args.d,
            console=args.c,
            tile=args.tile,
            invert=args.i,
            file=args.file,
            outputfile=outputfile,
            svg=args.svg,
            hexagon=args.hexagon,
            stroke=args.stroke,
            round=args.round,
            bg_color=args.background,
        )
    elif args.sha3:
        sha3_512_mode(
            input=args.input,
            bypass=args.bypass,
            debug=args.d,
            console=args.c,
            tile=args.tile,
            invert=args.i,
            file=args.file,
            outputfile=outputfile,
            svg=args.svg,
            hexagon=args.hexagon,
            stroke=args.stroke,
            round=args.round,
            bg_color=args.background,
        )
    elif args.blake2b:
        blake2b_mode(
            input=args.input,
            bypass=args.bypass,
            debug=args.d,
            console=args.c,
            tile=args.tile,
            invert=args.i,
            file=args.file,
            outputfile=outputfile,
            svg=args.svg,
            hexagon=args.hexagon,
            stroke=args.stroke,
            round=args.round,
            bg_color=args.background,
        )
    elif args.shake256:
        shake_256_mode(
            input=args.input,
            bypass=args.bypass,
            debug=args.d,
            console=args.c,
            tile=args.tile,
            invert=args.i,
            digest_length=args.length,
            file=args.file,
            outputfile=outputfile,
            svg=args.svg,
            hexagon=args.hexagon,
            stroke=args.stroke,
            round=args.round,
            bg_color=args.background,
        )
    elif args.md6:
        md6_mode(
            input=args.input,
            bypass=args.bypass,
            debug=args.d,
            console=args.c,
            tile=args.tile,
            invert=args.i,
            file=args.file,
            outputfile=outputfile,
            svg=args.svg,
            hexagon=args.hexagon,
            stroke=args.stroke,
            round=args.round,
            bg_color=args.background,
        )
    else:
        md5_mode(
            input=args.input,
            bypass=args.bypass,
            debug=args.d,
            console=args.c,
            tile=args.tile,
            invert=args.i,
            file=args.file,
            outputfile=outputfile,
            svg=args.svg,
            hexagon=args.hexagon,
            stroke=args.stroke,
            round=args.round,
            bg_color=args.background,
        )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
