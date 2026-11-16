import hashlib
import sys

from MD6 import MD6

from hashpic.util import (
    debug_log,
    file_to_hash,
    paint_png,
    print_to_console,
    svg_mode,
    validity_check,
)


def _run_mode(
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
    *,
    name,
    hash_text,
    hash_file,
    hash_length,
    size=0x400,
    first_argument_only=False,
    image_hash_suffix="",
):
    if file:
        if hash_file is None:
            raise NotImplementedError(f"Not implemented for {name}")
        hash_value = hash_file(file)
    else:
        from_stdin = not input
        hash_input = sys.stdin.read() if from_stdin else (
            input[0] if bypass or first_argument_only else " ".join(input)
        )
        hash_value = (
            hash_input.rstrip("\n").lower()
            if bypass
            else hash_text(hash_input, from_stdin)
        )

    validity_check(
        hash=hash_value,
        regex_str=rf"^[a-f0-9]{{{hash_length}}}$",
        name=name,
    )

    if debug:
        debug_log(input=input, hash=hash_value, bypass=bypass)

    hash_value += image_hash_suffix

    if svg:
        svg_mode(
            hash=hash_value,
            size=size,
            digest_length=len(hash_value) // 2,
            invert=invert,
            debug=debug,
            outputfile=outputfile,
            round=round,
            hexagon=hexagon,
            with_stroke=stroke,
            bg_color=bg_color,
        )

    if console:
        print_to_console(hash_value, invert, tile)

    paint_png(
        hash=hash_value,
        size=size,
        invert=invert,
        debug=debug,
        outputfile=outputfile,
    )


def _run_hashlib_mode(
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
    *,
    name,
    hash_factory,
    hash_length,
    digest_length=None,
    size=0x400,
    image_hash_suffix="",
):
    def hash_text(value, _):
        hasher = hash_factory()
        hasher.update(value.encode())
        return (
            hasher.hexdigest()
            if digest_length is None
            else hasher.hexdigest(digest_length)
        )

    def hash_file(file_path):
        return file_to_hash(file_path, hash_factory(), digest_length)

    _run_mode(
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
        name=name,
        hash_text=hash_text,
        hash_file=hash_file,
        hash_length=hash_length,
        size=size,
        image_hash_suffix=image_hash_suffix,
    )


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
    hexagon,
    stroke,
    round,
    bg_color,
):
    _run_hashlib_mode(
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
        name="MD5",
        hash_factory=hashlib.md5,
        hash_length=32,
    )


def sha_512_mode(
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
    _run_hashlib_mode(
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
        name="SHA512",
        hash_factory=hashlib.sha512,
        hash_length=128,
    )


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
    hexagon,
    stroke,
    round,
    bg_color,
):
    _run_hashlib_mode(
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
        name="SHA3-512",
        hash_factory=hashlib.sha3_512,
        hash_length=128,
    )


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
    _run_hashlib_mode(
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
        name="BLAKE2b",
        hash_factory=hashlib.blake2b,
        hash_length=128,
    )


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

    _run_hashlib_mode(
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
        name=f"SHAKE256-{variable_digest_length}",
        hash_factory=hashlib.shake_256,
        hash_length=variable_digest_length * 2,
        digest_length=variable_digest_length,
        size=1200,
        image_hash_suffix="ff" if variable_digest_length == 0xFF else "",
    )


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
    md6 = MD6(size=0x200)

    def hash_text(value, from_stdin):
        return str(md6(value.encode() if from_stdin else value))

    _run_mode(
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
        name="MD6",
        hash_text=hash_text,
        hash_file=None,
        hash_length=128,
        first_argument_only=True,
    )
