# CENG 488 Assignment6 by
# Elman Hamdi
# 240201036
# May 2021



import time

from cameras import *
from utils import *
from objects import *
from scenes import *
from views import *
import json

with open("file.json") as f:
    render_file = json.load(f)

render_settings = render_file['renderSettings']
WIDTH = render_settings['xres']
HEIGHT = render_settings['yres']
SAMPLE = render_settings['samples']

# init scene
# init scene
scene = Scene()
window = Window(HEIGHT, WIDTH)
camera = Camera(
    eye=Pos3d.list_to_pos(render_file['camera']['position']),
    center=Pos3d(0, 0, 0),
    window=window,
    window_distance=render_file['camera']['window_distance'],
)


for raw_sphere in render_file['sphere']:
    sphere = Sphere(
        radius=raw_sphere['radius'],
        center=Pos3d.list_to_pos(raw_sphere['position']),
        material=Material(
            color=Color(
                raw_sphere['color'][0],
                raw_sphere['color'][1],
                raw_sphere['color'][2],
            ),
        ),
    )
    scene.add(sphere)


view = View(camera=camera, scene=scene)


def main():


    #THREADED VERSION
    view.calculate_ambient_occusion_with_thread(sample=SAMPLE, nof_divide= 200, nof_thread=9)

    #UNTHREADED VERSION
    #view.draw_ambient_occlusion(SAMPLE)

    return 0


if __name__ == '__main__':
    main()
    
    


