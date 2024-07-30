import os
import random
from typing import List

import drawsvg as draw
import numpy as np
import shapely



MinBoardDs = 1000
MaxBoardDs = 10000

MinDensity = 0.5
MaxDensity = 1.0
Designs = 100
MaxConnections = 100

dx = np.random.randint(MinBoardDs, MaxBoardDs, Designs)
dy = np.random.randint(MinBoardDs, MaxBoardDs, Designs)
d = draw.Drawing(MaxBoardDs, MaxBoardDs)





class Label:
    def __init__(self, file: chr, score: float):
        self.filename = file
        self.score = score


def det_crosses(lines: List[shapely.LineString]):
    total = max(len(lines), 1)
    already_has_cross = set()

    crosses = 0;
    for idx in range (total-1):
        line1 = lines[idx]
        for jdx in range (idx+1,total):
            line2 = lines[jdx]
            if line2 in already_has_cross:
                continue
            intersect = line1.intersects(line2)
            if intersect:
                crosses += 1
                already_has_cross.add(line2)

    total = max (total, 1)
    return total, crosses


def straight_connection (design_idx):
    r = random.random(100)
    if r < 50:
        xfrom = np.random.randint(dx[design_idx])
        yfrom = np.random.randint(dy[design_idx])
        xto = np.random.randint(dx[design_idx])
        yto = yfrom
    else:
        xfrom = np.random.randint(dx[design_idx])
        yfrom = np.random.randint(dy[design_idx])
        xto = xfrom
        yto = np.random.randint(dy[design_idx])

    aline = shapely.LineString([(xfrom, yfrom), (xto, yto)])
    return aline

def random_connection (design_idx):
    xfrom = np.random.randint(dx[design_idx])
    yfrom = np.random.randint(dy[design_idx])

    xto = np.random.randint(dx[design_idx])
    yto = np.random.randint(dy[design_idx])
    aline = shapely.LineString([(xfrom, yfrom), (xto, yto)])
    return aline


def gen_connection (design_idx):
    r = random.random(100)
    if r < 50:
        return random_connection(design_idx)
    else:
        return straight_connection(design_idx)


def draw_board_outline (design_idx):
    line = draw.Line(0, 0, dx[design_idx], 0, stroke='red', stroke_width=10)
    d.append(line)
    line = draw.Line(dx[design_idx], 0, dx[design_idx], dy[design_idx], stroke='red', stroke_width=10)
    d.append(line)
    line = draw.Line(0, dy[design_idx], dx[design_idx], dy[design_idx], stroke='red', stroke_width=10)
    d.append(line)
    line = draw.Line(0, dy[design_idx], 0, 0, stroke='red', stroke_width=10)
    d.append(line)


def row_col_from_index (index)




def create_test_cases(labels: List[Label]):
    os.chdir("./images")
    for design_idx in range(Designs):

        d.clear()
        # r = draw.Rectangle(0, 0, dx[design_idx], dy[design_idx], fill='white')
        lines = []

        c = np.random.randint(MaxConnections)
        c = MaxConnections
        for cidx in range(c):
            aline = gen_connection(design_idx)
            lines.append(aline)
            line = draw.Line(aline[0][0], aline[0][1],aline[1][0],aline[1][1], stroke='blue', stroke_width=2)
            d.append(line)

        draw_board_outline(design_idx)

        total, crosses = det_crosses(lines)
        score = crosses / total

        filename = 't' + str(design_idx) + '.svg'

        label = Label(filename, score)
        labels.append(label)
        d.save_svg(filename)

    os.chdir("..")
    f = open("labels.csv", "w")

    for label in labels:
        s = label.filename + "," + str(label.score) + '\n'
        f.write(s)
    f.close()


labels = list()

create_test_cases(labels)

print('done')