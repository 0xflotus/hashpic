import sys, os, re
from math import sqrt
from .data import COLOR_DATA
from .config import BLOCKSIZE, RGB, AREA


def chunk_it(string, n=2):
    return [string[i : i + n] for i in range(0, len(string), n)]


def convert_term_to_rgb(color_code=0):
    return COLOR_DATA.get(color_code)["rgb"]


def print_to_console(hash, invert, tile):
    chunks = chunk_it(chunk_it(hash), int(sqrt(len(hash) / 2)))
    for chunk in chunks:
        for j in chunk:
            i = int(j, 16)
            sys.stdout.write(
                f"\033[38;5;{0xff - i if invert else i}"
                f"m{j if not tile else '▮'}\u001b[0m"
            )
        sys.stdout.write("\n")
    sys.exit(0)


def hash_to_color_codes(hash):
    return [convert_term_to_rgb(int(chunk, 16)) for chunk in chunk_it(hash)]


def paint_svg(size, digest_length, colors):
    SVG_DATA_HEADER = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="{size}" height="{size}">\n'
    )
    steps = int(size // (digest_length ** 0.5))
    store = [
        AREA(x, x + steps, y, y + steps)
        for y in range(0, size, steps)
        for x in range(0, size, steps)
    ]

    rects = [
        f'  <rect width="{steps}" height="{steps}" '
        f'fill="#{"".join(tuple(map(lambda cc: hex(cc)[2:].zfill(2), colors[idx])))}" '
        f'x="{x}" y="{y}"/>'
        for y in range(0, size, steps)
        for x in range(0, size, steps)
        for idx, (min_x, max_x, min_y, max_y) in enumerate(store)
        if min_x <= x < max_x and min_y <= y < max_y
    ]
    return SVG_DATA_HEADER + "\n".join(rects) + "\n</svg>\n"


def svg_mode(hash, size, digest_length, invert, debug, outputfile):
    color_codes = hash_to_color_codes(hash)
    if invert:
        color_codes = [RGB(r ^ 0xFF, g ^ 0xFF, b ^ 0xFF) for r, g, b in color_codes]
    SVG = paint_svg(size=size, digest_length=digest_length, colors=color_codes)

    if debug:
        sys.stdout.write(SVG)
        sys.exit(0)

    filename = os.getcwd() + "/" + outputfile
    f = open(filename, "w")
    f.write(SVG)
    f.close()
    sys.exit(0)


def debug_log(input, hash, bypass):
    sys.stdout.write(
        f'hashpic: "{input}" will be following hash: {hash}\n'
        if not bypass
        else f"hashpic: directly given hash: {input}\n"
    )


def validity_check(hash, regex_str, name):
    pattern = re.compile(regex_str)
    match = pattern.match(hash)
    if not match:
        sys.stderr.write(f"{hash} is not a valid {name} hash\n")
        sys.exit(-1)


def file_to_hash(file, hasher, digest_length=None):
    with open(file, "rb") as tfile:
        while True:
            buffer = tfile.read(BLOCKSIZE)
            hasher.update(buffer)
            if len(buffer) <= 0:
                break
    if digest_length:
        return hasher.hexdigest(digest_length).lower()
    else:
        return hasher.hexdigest().lower()
