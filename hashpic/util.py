import sys, os, re
from math import sqrt, sin, cos, pi
from PIL import Image, ImageOps, ImageDraw
from hashpic.data import COLOR_DATA
from hashpic.config import BLOCKSIZE, RGB, AREA


def chunk_it(string, n=2):
    return [string[i : i + n] for i in range(0, len(string), n)]


def convert_term_to_rgb(color_code=0):
    return COLOR_DATA.get(color_code)["rgb"]


def print_to_console(hash, invert, tile):
    chunks = chunk_it(chunk_it(hash), int((len(hash) >> 1) ** 0.5))
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


def paint_svg(size, digest_length, colors, rounded_corners=False, bg_color=None):
    SVG_DATA_HEADER = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="{size}" height="{size}"'
    )
    SVG_DATA_HEADER += (
        f' style="background-color: {bg_color}">\n' if bg_color else ">\n"
    )

    steps = int(size // (digest_length ** 0.5))
    store = [
        AREA(x, x + steps, y, y + steps)
        for y in range(0, size, steps)
        for x in range(0, size, steps)
    ]

    rx = steps >> 1 if rounded_corners else 0
    rects = [
        f'  <rect width="{steps}" height="{steps}" '
        f'fill="#{"".join(map(lambda _: format(_, "02x"), colors[idx]))}" '
        f'x="{x}" y="{y}" rx="{rx}"/>'
        for y in range(0, size, steps)
        for x in range(0, size, steps)
        for idx, (min_x, max_x, min_y, max_y) in enumerate(store)
        if min_x <= x < max_x and min_y <= y < max_y
    ]
    return SVG_DATA_HEADER + "\n".join(rects) + "\n</svg>\n"


def svg_mode(
    hash,
    size,
    digest_length,
    invert,
    debug,
    outputfile,
    round,
    hexagon,
    with_stroke,
    bg_color,
):
    color_codes = hash_to_color_codes(hash)
    if invert:
        color_codes = [RGB(r ^ 0xFF, g ^ 0xFF, b ^ 0xFF) for r, g, b in color_codes]

    if hexagon:
        SVG = hexagons(
            dimension=int(sqrt(digest_length)),
            colors=color_codes,
            bg_color=bg_color,
            with_stroke=with_stroke,
        )
    else:
        SVG = paint_svg(
            size=size,
            digest_length=digest_length,
            colors=color_codes,
            rounded_corners=round,
            bg_color=bg_color,
        )

    if debug:
        sys.stdout.write(SVG)
        sys.exit(0)

    filename = os.getcwd() + "/" + outputfile
    f = open(filename, "w")
    f.write(SVG)
    f.close()
    sys.exit(0)


def hexagons(dimension, colors, bg_color=None, with_stroke=False):
    def hexpoints(x, y, radius):
        return " ".join(
            [
                f"{x + radius * sin(theta)},{y + radius * cos(theta)}"
                for theta in frange(0, pi * 2, pi / 3)
            ]
        )

    SIZES = {
        1: 390,
        2: 190,
        3: 133,
        4: 90,
        5: 70,
        6: 66,
        8: 50,
        10: 40,
        12: 33,
        15: 26,
        16: 30,
    }

    SVG_HEADER = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n'
        '<svg version="1.1"'
        ' width="900" height="800"'
        ' xmlns="http://www.w3.org/2000/svg"'
    )
    SVG_HEADER += f' style="background-color: {bg_color}">\n' if bg_color else ">\n"

    stroke = "stroke: black; stroke-width: 3px;" if with_stroke else ""
    polygons = []
    radius = SIZES[dimension]
    for i in range(0, dimension):
        for j in range(0, dimension):
            offset = (sqrt(3) * radius) / 2
            x = (radius + 10) + offset * i * 2
            y = (radius + 10) + offset * j * sqrt(3)

            if j % 2 != 0:
                x += offset
            polygons.append(
                f'  <polygon style="fill: #{"".join(map(lambda _: format(_, "02x"), colors[j * dimension + i % dimension]))}; '
                f'{stroke}" points="{hexpoints(x, y, radius)}"></polygon>'
            )
    SVG = "\n".join(polygons)
    return SVG_HEADER + SVG + "\n</svg>"


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


def paint_png(hash, size, invert, debug, outputfile):
    colors = hash_to_color_codes(hash)

    im = Image.new(mode="RGB", size=(size, size), color="#ffffff")
    draw = ImageDraw.Draw(im)
    m_size = int((len(hash) >> 1) ** 0.5)
    steps = int(size // m_size)
    store = [
        (i, steps * (row + 1), i + steps, steps * row)
        for row in range(m_size)
        for i in range(0, size, steps)
    ]

    for idx, xy in enumerate(store):
        draw.rectangle(xy, fill=colors[idx])
    del idx, xy

    if invert:
        im = ImageOps.invert(im)

    if debug:
        im.show()

    im.save(os.getcwd() + "/" + outputfile)
    sys.exit(0)


"""
Helper function to use floats in range function
"""


def frange(start, stop=None, step=None):
    start = float(start)
    if stop == None:
        stop = start + 0.0
        start = 0.0
    if step == None:
        step = 1.0

    count = 0
    while True:
        temp = float(start + count * step)
        if step > 0 and temp >= stop:
            break
        elif step < 0 and temp <= stop:
            break
        yield temp
        count += 1
