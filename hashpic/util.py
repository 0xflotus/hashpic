import json
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


def hash_to_color_codes(hash):
    return [convert_term_to_rgb(int(chunk, 16)) for chunk in chunk_it(hash)]


def paint_svg(size, digest_length, colors):
    def colorcode_to_hex(color_code):
        return hex(color_code)[2:].zfill(2)

    SVG_DATA = """<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
    <svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="1200" height="1200">
    """
    steps = int(size // (int(digest_length) ** 0.5))
    store = []
    for x in range(0, size, steps):
        for y in range(0, size, steps):
            store.append([y, y + steps, x, x + steps])

    for x in range(0, size, steps):
        for y in range(0, size, steps):
            for line, idx in zip(store, range(len(store))):
                if line[0] <= x < line[1] and line[-2] <= y < line[-1]:
                    SVG_DATA += f"""<rect width="{steps}" height="{steps}" fill="#{colorcode_to_hex(colors[idx][0])}{colorcode_to_hex(colors[idx][1])}{colorcode_to_hex(colors[idx][2])}" x="{x}" y="{y}"/>\n"""
    SVG_DATA += """</svg>\n"""
    return SVG_DATA
