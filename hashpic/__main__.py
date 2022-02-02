import argparse
from .md5 import *
from .sha512 import *
from .shake256 import *


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
    parser.add_argument("--length", action="store")
    args = parser.parse_args()

    if args.sha512:
        sha_512_mode(
            input=args.input,
            bypass=args.bypass,
            debug=args.d,
            console=args.c,
            invert=args.i,
        )
    elif args.shake256:
        shake_256_mode(
            input=args.input,
            bypass=args.bypass,
            debug=args.d,
            console=args.c,
            invert=args.i,
            digest_length=args.length,
        )
    else:
        md5_mode(
            input=args.input,
            bypass=args.bypass,
            debug=args.d,
            console=args.c,
            invert=args.i,
        )


if __name__ == "__main__":
    main()
