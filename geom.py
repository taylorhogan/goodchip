import copy


class XY:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

class Rect:
    def __init__(self, ll, ur):
        self.ll = ll
        self.ur = ur

    def move_by(self, x, y):
        r = copy.deepcopy(self)
        r.ll.x = self.ll.x + x
        r.ll.y = self.ll.y + y
        r.ur.x = self.ur.x + x
        r.ur.y = self.ur.y + y
        return r

    def width(self):
        return abs(self.ur.x - self.ll.x)

    def height(self):
        return abs(self.ur.y - self.ll.y)

    def center(self):
        return XY(self.ll.x+self.width()/2, self.ll.y+self.height()/2)
