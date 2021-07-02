# CENG 488 Assignment6 by
# Elman Hamdi
# 240201036
# May 2021

from utils import *


class Ray:
    def __init__(self, start_pos=Pos3d(0, 0, 0, 1), direction=Vec3d(1, 1, 1, 0)):
        self.start_pos = start_pos
        self.direction = direction

    @property
    def start_pos(self):
        return self.__start_pos

    @start_pos.setter
    def start_pos(self, start_pos):
        self.__start_pos = start_pos

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, direction):
        self.__direction = direction
