import numpy

class pos2:
    def __init__(self, x: int = None, y: int = None, dtype = None) -> None:
        self.dtype = dtype
        try:
            if x == None and y == None:
                self.x = 0
                self.y = 0
                return
        except:
            self.x = x[0]
            self.y = x[1]
            return
        else:
            self.x = x
            self.y = y
    def getVector(self):
        return numpy.array([self.x, self.y], dtype = self.dtype)
    def __repr__(self) -> str: return f"pos2 [{self.x}, {self.y}]"

class size2:
    def __init__(self, w: int = None, h: int = None, dtype = None) -> None:
        self.dtype = dtype
        if w == None and h == None:
            self.w = 0
            self.h = 0
        elif h == None:
            self.w = w[0]
            self.h = w[1]
        else:
            self.w = w
            self.h = h
    def getVector(self):
        return numpy.array([self.w, self.h], dtype = self.dtype)
    def __repr__(self) -> str: return f"size2 [{self.w}, {self.h}]"
