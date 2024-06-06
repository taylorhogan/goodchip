import os
from typing import List

import drawsvg as draw
import numpy as np

MinBoardDs = 1000
MaxBoardDs = 10000

MinDensity = 0.5
MaxDensity = 1.0
Designs = 1000
MaxConnections = 1000

dx = np.random.randint(MinBoardDs, MaxBoardDs, Designs)
dy = np.random.randint(MinBoardDs, MaxBoardDs, Designs)
d = draw.Drawing(MaxBoardDs, MaxBoardDs)


class Line:
    def __init__(self, x0: int, y0: int, x1: int, y1: int):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1


class Label:
    def __init__(self, file: chr, score: float):
        self.filename = file
        self.score = score


def det_crosses(lines: List[Line]):
    total = max(len(lines), 1)
    crosses = np.random.randint(0, total)
    return total, crosses


def create_test_cases(labels: List[Label]):
    os.chdir("/Users/taylorhogan/Documents/Development/goodchip/images")
    for design in range(Designs):

        d.clear()
        r = draw.Rectangle(0, 0, dx[design], dy[design], fill='white')
        lines = []

        c = np.random.randint(MaxConnections)
        for cidx in range(c):
            xfrom = np.random.randint(dx[design])
            xto = np.random.randint(dx[design])
            yfrom = np.random.randint(dy[design])
            yto = np.random.randint(dy[design])
            aline = Line(xfrom, yfrom, xto, yto)
            lines.append(aline)
            line = draw.Line(xfrom, yfrom, xto, yto, stroke='blue', stroke_width=2)
            d.append(line)

        line = draw.Line(0, 0, dx[design], 0, stroke='red', stroke_width=10)
        d.append(line)
        line = draw.Line(dx[design], 0, dx[design], dy[design], stroke='red', stroke_width=10)
        d.append(line)
        line = draw.Line(0, dy[design], dx[design], dy[design], stroke='red', stroke_width=10)
        d.append(line)
        line = draw.Line(0, dy[design], 0, 0, stroke='red', stroke_width=10)
        d.append(line)

        total, crosses = det_crosses(lines)
        score = crosses / total

        filename = 't' + str(design) + '.svg'

        label = Label(filename, score)
        labels.append(label)
        d.save_svg(filename)

    os.chdir("/Users/taylorhogan/Documents/Development/goodchip")
    f = open("labels.csv", "w")

    for label in labels:
        s = label.filename + "," + str(label.score) + '\n'
        f.write(s)
    f.close()


labels = list()

create_test_cases(labels)

print('done')