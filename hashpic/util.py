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
