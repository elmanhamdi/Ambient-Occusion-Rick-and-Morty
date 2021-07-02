from utils import *


class Light:
    def __init__(self, lightPos=Pos3d(0, 0, 0), lightColor=[1, 1, 1, 1], lightIntensity=1):
        self.lightPos = lightPos
        self.lightColor = lightColor
        self.lightIntensity = lightIntensity


class Color:
    def __init__(self, r, g, b, a):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def __str__(self):
        return '[' + self.r + ', ' + self.g + ', ' + self.b + ', ' + self.a + ']'
