from collections import namedtuple

BLOCKSIZE = 0x1000
RGB = namedtuple("RGB", ["r", "g", "b"])
AREA = namedtuple("area", ["min_x", "max_x", "min_y", "max_y"])
