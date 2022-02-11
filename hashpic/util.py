import json, sys, os, re
from math import sqrt
from .data import *


def chunk_it(string, n=2):
    return [string[i : i + n] for i in range(0, len(string), n)]


def convert_term_to_rgb(color_code=0):
    data = json.loads(COLOR_DATA)
    s_cc = (0, 0, 0)
    for i in data:
        if data[i]["term"] == str(color_code):
            s_cc = tuple([int(i) for i in data[i]["rgb"][4:-1].split(",")])
    return s_cc


def print_to_console(hash, invert, tile):
    chunks = chunk_it(chunk_it(hash), int(sqrt(len(hash) / 2)))
    for i in chunks:
        for j in i:
            sys.stdout.write(
                f"\033[38;5;{0xff - int(j, 16) if invert else int(j, 16)}m{j if not tile else '▮'}\u001b[0m"
            )
        sys.stdout.write("\n")
    sys.exit(0)


def hash_to_color_codes(hash):
    return [convert_term_to_rgb(int(chunk, 16)) for chunk in chunk_it(hash)]


def paint_svg(size, digest_length, colors):
    def colorcode_to_hex(color_code):
        return hex(color_code)[2:].zfill(2)

    SVG_DATA = f"""<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
    <svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="{size}" height="{size}">
    """
    steps = int(size // (int(digest_length) ** 0.5))
    store = []
    for x in range(0, size, steps):
        for y in range(0, size, steps):
            store.append([y, y + steps, x, x + steps])

    for x in range(0, size, steps):
        for y in range(0, size, steps):
            for idx, line in enumerate(store):
                if line[0] <= x < line[1] and line[-2] <= y < line[-1]:
                    SVG_DATA += f"""<rect width="{steps}" height="{steps}" fill="#{colorcode_to_hex(colors[idx][0])}{colorcode_to_hex(colors[idx][1])}{colorcode_to_hex(colors[idx][2])}" x="{x}" y="{y}"/>\n"""
    SVG_DATA += """</svg>\n"""
    return SVG_DATA


def svg_mode(hash, size, digest_length, invert, debug, outputfile):
    color_codes = hash_to_color_codes(hash)
    if invert:
        color_codes = list(
            map(lambda cc: (cc[0] ^ 0xFF, cc[1] ^ 0xFF, cc[2] ^ 0xFF), color_codes)
        )
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
