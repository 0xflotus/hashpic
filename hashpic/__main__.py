import argparse
from .md5 import *
from .sha512 import *
from .shake256 import *
from .blake2b import *
from .sha3 import *


def main():
    parser = argparse.ArgumentParser(
        description="Create an image from a MD5 or SHA512 hash"
    )
    parser.add_argument("input", nargs="*", action="store", help="Input string to hash")
    parser.add_argument("-d", action="store_true", help="debug mode")
    parser.add_argument("-i", action="store_true", help="invert the image")
    parser.add_argument("--bypass", action="store_true", help="give a hash directly")
    parser.add_argument("-c", action="store_true", help="console mode")
    parser.add_argument("--sha512", action="store_true")
    parser.add_argument("--shake256", action="store_true")
    parser.add_argument("--sha3", action="store_true")
    parser.add_argument("--blake2b", action="store_true")
    parser.add_argument("--length", action="store")
    parser.add_argument("--file", action="store")
    parser.add_argument("--slow", action="store_true")
    parser.add_argument("-o", action="store", default="output.png")
    args = parser.parse_args()

    if args.sha512:
        sha_512_mode(
            input=args.input,
            bypass=args.bypass,
            debug=args.d,
            console=args.c,
            invert=args.i,
            file=args.file,
            outputfile=args.o,
        )
    elif args.sha3:
        sha3_512_mode(
            input=args.input,
            bypass=args.bypass,
            debug=args.d,
            console=args.c,
            invert=args.i,
            file=args.file,
            outputfile=args.o,
        )
    elif args.blake2b:
        blake2b_mode(
            input=args.input,
            bypass=args.bypass,
            debug=args.d,
            console=args.c,
            invert=args.i,
            file=args.file,
            outputfile=args.o,
        )
    elif args.shake256:
        shake_256_mode(
            input=args.input,
            bypass=args.bypass,
            debug=args.d,
            console=args.c,
            invert=args.i,
            digest_length=args.length,
            file=args.file,
            outputfile=args.o,
            slow_mode=args.slow
        )
    else:
        md5_mode(
            input=args.input,
            bypass=args.bypass,
            debug=args.d,
            console=args.c,
            invert=args.i,
            file=args.file,
            outputfile=args.o,
        )


if __name__ == "__main__":
    main()
