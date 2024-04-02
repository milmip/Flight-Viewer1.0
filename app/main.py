'''
Code source of -Flight Viewer-, Emilien Progin 03.24
'''

import os
import sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import numpy as np
from time import sleep
from toml import loads

import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from scene import Scene
from camera import Camera


class App:
    def __init__(self, config_data):

        self.win_size = config_data['win_size']
        self.init_graphic_engine(config_data)

        self.clock = pg.time.Clock()
        self.wait = 1000

        self.keys_pressed = None
        self.mouse_motion = None
        self.mouse_pos = None
        self.focus = False
        self.freeze = False
        
        self.light_position = np.array(config_data['light_pos'])
        self.scene = Scene(self, config_data)
        
        self.camera = Camera(self)

        print("\nPress 'h' for help")

    def init_graphic_engine(self, config_data):
        pg.init()
        pg.display.set_mode(self.win_size, DOUBLEBUF|OPENGL)
        pg.display.set_caption('Flight Viewer')
        pg.mouse.set_visible(False)

        r, g, b, a = (np.array(config_data['sky_col'])/255).tolist()
        glClearColor(r, g, b, a)

        gluPerspective(70, self.win_size[0]/self.win_size[1], 0.1, 50.0)

        glDisable(GL_TEXTURE_2D)
        glDisable(GL_DEPTH_TEST)

        loading_image = pg.image.load(os.path.join('img', 'loading_img.png'))
        glWindowPos2dv((0,0))
        glDrawPixels(self.win_size[0], self.win_size[1], GL_RGBA, GL_UNSIGNED_BYTE, 
                    pg.image.tostring(loading_image, "RGBA", True))
        pg.display.flip()

        glEnable(GL_TEXTURE_2D)
        glEnable(GL_DEPTH_TEST)

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        self.scene.render()
        pg.display.flip()

    def check_event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.kill()
            if event.type == pg.KEYDOWN:
                self.scene.update(event.key)

        self.keys_pressed = pg.key.get_pressed()
        self.mouse_motion = pg.mouse.get_rel()
        self.mouse_pos = pg.mouse.get_pos()

        if self.focus:
            self.mouse_motion = (0,0)
            self.focus = False
        elif self.mouse_motion == (0,0) or not 100 < self.mouse_pos[0] < self.win_size[0] - 100 or not 100 < self.mouse_pos[1] < self.win_size[1] - 100:
            pg.mouse.set_pos(self.win_size[0] / 2, self.win_size[1] / 2)
            self.focus = True
    
    def update(self):
        if True in self.keys_pressed or self.mouse_motion != (0,0):
            self.wait = 0
        self.camera.update()
        self.wait += 1

    def tick(self):
        self.clock.tick(60)

    def kill(self):
        pg.quit()
        sys.exit()
                    
    def run(self):
        while True:

            self.check_event()
            self.update()
            if not self.freeze:
                self.render()
            self.tick()



def load_toml():
    with open(os.path.join('..', 'config.toml'), 'r') as f:
        toml_data = loads(f.read())
    return toml_data

if __name__ == '__main__':
    config = load_toml()
    application = App(config)
    application.run()