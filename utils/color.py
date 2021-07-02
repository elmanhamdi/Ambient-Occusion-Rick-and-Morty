# CENG 488 Assignment6 by
# Elman Hamdi
# 240201036
# May 2021s

class Color:
    def __init__(self, r, g, b, a = 255):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def __str__(self):
        return '[' + self.r + ', ' + self.g + ', ' + self.b + ', ' + self.a + ']'

    def __mul__(self, other):
        self.r *= other
        self.g *= other
        self.b *= other
        self.a *= other

    def getRGB(self):
        return [self.r, self.g, self.b]
