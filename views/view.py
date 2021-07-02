# CENG 488 Assignment6 by
# Elman Hamdi
# 240201036
# May 2021


from utils import *
from objects import *
import numpy as np
import sys
from PIL import Image
from multiprocessing import Pool
import multiprocessing as mp
from itertools import product
from multiprocessing import Process
from transformations.transformations import Transformations
import random
from functools import partial


class View:
    def __init__(self, camera, scene=None, bgColor = Color(0,0,0, 1)):
        self.camera = camera
        self.scene = scene
        self.bgColor = bgColor

    def draw_a_list(self, pixel_list, open_after_draw=1, file_name='img'):
        img = Image.fromarray(pixel_list, 'RGB')
        img.save(file_name + '.png')
        if open_after_draw:
            img.close()
            Image.open(file_name + '.png').show()

    def draw_ambient_occlusion(self, sample, open_after_draw=1, file_name='img'):
        pixel_list = self.calculate_ambient_occlusion(sample)

        img = Image.fromarray(pixel_list, 'RGB')
        img.save(file_name + '.png')
        if open_after_draw:
            img.close()
            Image.open(file_name + '.png').show()

    def calculate_ambient_occlusion(self, sample):
        cam_h = self.camera.window.height
        cam_w = self.camera.window.width
        pixel_list = np.full((cam_h, cam_w, 3), fill_value=self.bgColor.getRGB(), dtype=np.uint8)

        for y in range(cam_h):
            View.__print_persantage(self, y, cam_h)

            for x in range(cam_w):

                pos_on_window = Pos3d.add(self.camera.eye,
                                          Pos3d(-cam_w / 2 + x, cam_h / 2 - y, self.camera.window_distance))

                ray_direction = HomogeneusCoor.normalize(Vec3d.positions_to_vec(pos_on_window, self.camera.eye))

                ray = Ray(start_pos=pos_on_window, direction=ray_direction)

                closest_node = None
                shortest = -1

                for node in self.scene.nodes:
                    intersect_tmp = node.intersect(ray)
                    if (intersect_tmp != -1):
                        if (intersect_tmp.t0 >= 0):
                            d = Pos3d.cal_distance_value(intersect_tmp.p0, pos_on_window)
                            if (shortest == -1) or (shortest > d):
                                shortest = d
                                closest_node = node
                                intersect = intersect_tmp

                if closest_node != None:
                    nof_intersect = 0
                    point = intersect.p0
                    for r in range(sample):

                        sample_ray = closest_node.generate_random_hemisphere_ray(point)

                        for n in self.scene.nodes:
                            if n != closest_node:
                                int_sample = n.intersect(sample_ray)
                                if (int_sample != -1) :
                                    if(int_sample.t0 > 0):
                                        nof_intersect += 1
                                        break

                        new_color = [x * ((sample - nof_intersect) / sample) for x in closest_node.material.color.getRGB()]
                        pixel_list[y][x] = new_color

        return pixel_list

    def __print_persantage(self, y, cam_h):
        persentage = ((y + 1) / cam_h) * 100

        a = ("%.2f" % persentage)
        # loading = ['/', '-', '\\','|', '/', '-','\\','|',]
        ENDC = '\033[0m'
        WARNING = '\033[93m'
        # sys.stdout.write('\r' +'  %' + a + ' ' + f'{WARNING}loading {ENDC}' + '.'*(y%5))
        sys.stdout.write('\r' + '  %' + a + ' ' + WARNING + 'loading' + ENDC + '.' * (y % 5))

    def __print_thread(self, thread_order, nof_thread,  cam_h):

        # loading = ['/', '-', '\\','|', '/', '-','\\','|',]
        ENDC = '\033[0m'
        WARNING = '\033[93m'
        # sys.stdout.write('\r' +'  %' + a + ' ' + f'{WARNING}loading {ENDC}' + '.'*(y%5))
        sys.stdout.write(
            '\r' "Total num of thread: " + str(nof_thread) +' -    ' +'Thread ' + str(thread_order) + ' ' + WARNING + 'is started' + ENDC )

    def ac_thread(self, nof_divide=5, sample=5, thread_order=1):

        cam_h = self.camera.window.height
        cam_w = self.camera.window.width
        pixel_list = np.full((cam_h, cam_w, 3), fill_value=self.bgColor.getRGB(), dtype=np.uint8)
        
        View.__print_thread(self, thread_order, nof_divide,  cam_h)
        for y in range(int(thread_order * cam_h / (nof_divide +1)), int((thread_order + 1) * cam_h / (nof_divide+ 1))):
            
            for x in range(cam_w):

                pos_on_window = Pos3d.add(self.camera.eye,
                                          Pos3d(-cam_w / 2 + x, cam_h / 2 - y, self.camera.window_distance))

                ray_direction = HomogeneusCoor.normalize(Vec3d.positions_to_vec(pos_on_window, self.camera.eye))

                ray = Ray(start_pos=pos_on_window, direction=ray_direction)

                closest_node = None
                shortest = -1

                for node in self.scene.nodes:
                    intersect_tmp = node.intersect(ray)
                    if (intersect_tmp != -1):
                        if (intersect_tmp.t0 >= 0):
                            d = Pos3d.cal_distance_value(intersect_tmp.p0, pos_on_window)
                            if (shortest == -1) or (shortest > d):
                                shortest = d
                                closest_node = node
                                intersect = intersect_tmp

                if closest_node != None:
                    nof_intersect = 0
                    point = intersect.p0
                    for r in range(sample):
                        sample_ray = closest_node.generate_random_hemisphere_ray(point)

                        for n in self.scene.nodes:
                            if n != closest_node:
                                int_sample = n.intersect(sample_ray)
                                if (int_sample != -1) :
                                    if(int_sample.t0 > 0):
                                        nof_intersect += 1
                                        break


                    new_color = [x * ((sample- nof_intersect) / sample) for x in closest_node.material.color.getRGB()]
                    pixel_list[y][x] = new_color

        return pixel_list

    def calculate_ambient_occusion_with_thread(self, nof_thread=5, nof_divide = 2, sample=5):

        parameters = []
        for i in range(nof_divide):
            parameters.append(i + 1)
            parameters.append(nof_divide)
            parameters.append(sample)

        func = partial(self.ac_thread, nof_divide, sample)

        with Pool(processes=nof_thread) as pool:
            results = pool.map(func, list(range(1, nof_divide + 1)))

        lst = results[0]
        for i in range(1, len(results)):
            lst = lst + results[i]

        self.draw_a_list(lst)



