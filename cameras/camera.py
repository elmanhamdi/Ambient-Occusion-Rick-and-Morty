# CENG 488 Assignment5 version2 by
# Elman Hamdi
# 240201036
# May 2021

import time

from utils.vec3d import Vec3d
from cameras.window import Window


import numpy


class Camera:

    def __init__(self, eye, center, window =Window(100,200), window_distance = 100):
        self.eye = eye
        self.center = center
        self.up = Vec3d(1, 0, 0)
        self.window = window
        self.window_distance = window_distance
