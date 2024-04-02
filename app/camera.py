from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import pygame as pg
from model import Topo, Track

class Camera():

    def __init__(self, APP, elevation=60, azimute=0):
        self.app = APP
        self.el = 90 - elevation
        self.az = azimute
        self.motions = [[pg.K_RIGHT, self.rotate_z, -1], [pg.K_LEFT, self.rotate_z, 1],
                    [pg.K_DOWN, self.rotate_x, -1], [pg.K_UP, self.rotate_x, 1],
                    [pg.K_w, self.translate_x, -0.05], [pg.K_s, self.translate_x, 0.05],
                    [pg.K_a, self.translate_y, -0.05], [pg.K_d, self.translate_y, 0.05],
                    [pg.K_SPACE, self.translate_z, -0.05], [pg.K_LALT, self.translate_z, 0.05]]
        self.dVec = np.array((np.sin(np.pi / 180 * self.az), np.cos(np.pi / 180 * self.az), 0))

        self.set_init_position()
        self.postion = np.array([5., 0., 3.])
        

    def set_init_position(self):
        
        glRotatef(90 - self.el, -1, 0, 0)
        glRotatef(self.az, 0, 0, 1)
        glTranslate(-5, 0, -3)


    def update(self):
        keys_pressed = self.app.keys_pressed
        if self.app.wait > 25:
            Topo.set_resolution(1)
            Track.set_resolution(1)

        for i in range(len(self.motions)):
            if keys_pressed[self.motions[i][0]]:
                self.app.freeze = False
                Topo.set_resolution(0)
                Track.set_resolution(0)
                self.motions[i][1](self.motions[i][2])

        if self.app.mouse_motion != (0,0):
            z, x = self.app.mouse_motion
            self.app.freeze = False
            Topo.set_resolution(0)
            Track.set_resolution(0)
            self.rotate_x(x/10)
            self.rotate_z(z/10)
        

    def translate_x(self, dist):
        self.dVec = np.array((np.sin(np.pi / 180 * self.az), np.cos(np.pi / 180 * self.az), 0))
        x, y, z = (self.dVec * dist).tolist()
        glTranslate(x, y, z)
        self.postion -= self.dVec * dist

    def translate_y(self, dist):
        self.dVec = np.array((-np.cos(np.pi / 180 * self.az), np.sin(np.pi / 180 * self.az), 0))
        x, y, z = (self.dVec * dist).tolist()
        glTranslate(x, y, z)
        self.postion -= self.dVec * dist

    def translate_z(self, dist):
        glTranslate(0, 0, dist)
        self.postion[2] -= dist

    def rotate_z(self, angle):
        self.az += angle
        self.az %= 360
        
        glTranslate(self.postion[0], self.postion[1], self.postion[2])
        glRotatef(angle, 0, 0, 1)
        glTranslate(-self.postion[0], -self.postion[1], -self.postion[2])

    def rotate_x(self, angle):
        if -90 <= self.el + angle <= 90:
            self.el += angle
            glTranslate(self.postion[0], self.postion[1], self.postion[2])
            glRotatef(self.az, 0, 0, -1)
            glRotatef(angle, 1, 0, 0)
            glRotatef(self.az, 0, 0, 1)
            glTranslate(-self.postion[0], -self.postion[1], -self.postion[2])