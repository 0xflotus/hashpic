import math
import numpy as np


def hexagons():
    print(
        '<svg id="s" version="1.1"'
        'width="300" height="300"'
        'xmlns="http://www.w3.org/2000/svg">'
    )

    radius = 30
    for i in range(0, 4):
        for j in range(0, 4):
            offset = (math.sqrt(3) * radius) / 2
            x = 40 + offset * i * 2
            y = 40 + offset * j * math.sqrt(3)

            if j % 2 != 0:
                x += offset
            print(
                f'<polygon style="fill: white; stroke: black; stroke-width: 4px;" points="{hexpoints(x,y,radius)}"></polygon>'
            )
    print("</svg>")


def hexpoints(x, y, radius):
    points = []
    for theta in np.arange(0, math.pi * 2, math.pi / 3):
        point_x = x + radius * math.sin(theta)
        point_y = y + radius * math.cos(theta)
        points.append(str(point_x) + "," + str(point_y))
    return " ".join(points)


hexagons()
