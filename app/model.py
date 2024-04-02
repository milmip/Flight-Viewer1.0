from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import pygame as pg
import sys
from os.path import join


class Help:
    def __init__(self, app):
        self.app = app
        self.hide = True
        self.img_commands = pg.image.load(join('img', 'commands.jpg'))
        self.commands = pg.image.tostring(self.img_commands, "RGBA", True)

    def render(self):
        if self.hide:
            return
        
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_DEPTH_TEST)

        glWindowPos2dv([0, self.app.win_size[1] - 218])
        glDrawPixels(500, 218, GL_RGBA, GL_UNSIGNED_BYTE, self.commands)

        glEnable(GL_TEXTURE_2D)
        glEnable(GL_DEPTH_TEST)

class Minimap:
    def __init__(self, app, size_factor):
        self.app = app
        self.dim = 500
        self.position = [self.app.win_size[0] - self.dim - 20, 20]
        self.size_factor = size_factor

        self.img_point = pg.image.load(join('img', 'point.png'))
        self.point = pg.image.tostring(self.img_point, "RGBA", True)

        self.images = self.get_images(join('map', 'swiss-map-raster25_2020_1225_krel_1.25_2056.tif'))
        
        self.dif_scales = 5
        
        self.corner_coord = np.array((2_567_500, 1_170_000))
        self.map_size = np.array((17_500, -12_000))
        
        self.surface = pg.Surface((self.dim, self.dim))

        self.hide = False
        self.zoom = 0

    def get_images(self, filename):
        scales = [1, 0.8, 0.6, 0.4, 0.2]
        img = pg.image.load(filename)
        img_px_dim = np.array((img.get_width(), img.get_height()))

        return [ (pg.transform.scale(img, img_px_dim * i), img_px_dim * i) for i in scales ]

    def set_zoom(self, scale):
        if 0 <= self.zoom + scale <= self.dif_scales - 1:
            self.zoom += scale

    def get_camera_coord(self):
        return np.array((self.app.camera.postion * 1/self.size_factor + Track.translate_vec)[:2])

    def get_map_motion_coord(self):
        return self.images[self.zoom][1] * (self.get_camera_coord() - self.corner_coord) / self.map_size

    def recenter(self):
        move_X, move_Y = self.get_map_motion_coord() - self.dim/2
        
        self.surface.blit(self.images[self.zoom][0], (0, 0), (move_X, move_Y, self.dim, self.dim))
        self.minimap_image = pg.image.tostring(self.surface, "RGBA", True)
        
        

    def render(self):
        if self.hide:
            return
        self.recenter()
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_DEPTH_TEST)

        glWindowPos2dv(self.position)
        glDrawPixels(self.dim, self.dim, GL_RGBA, GL_UNSIGNED_BYTE, self.minimap_image)

        glWindowPos2dv([self.app.win_size[0] - self.dim - 30 + self.dim/2, 20 + self.dim/2 - 10])
        glDrawPixels(20, 20, GL_RGBA, GL_UNSIGNED_BYTE, self.point)

        glEnable(GL_TEXTURE_2D)
        glEnable(GL_DEPTH_TEST)

class Track:
    ground_tiles = []
    resolution = 1
    translate_vec = None
    extended_tiles = []
    color = []

    def __init__(self, filename, size_factor):
        self.size_factor = size_factor
        self.vertex = [self.getVertexData(filename, 'ld'), self.getVertexData(filename, 'hd')]
        self.vertex_shadow = [self.getVertexData_shadow('ld'), self.getVertexData_shadow('hd')]
        self.fill_ground_rectangle()

    @classmethod
    def fill_ground_rectangle(cls):
        x_min, y_min = cls.ground_tiles.pop()
        x_max = x_min
        y_max = y_min

        for i in range(len(cls.ground_tiles)):
            x, y = cls.ground_tiles.pop()
            if x > x_max:
                x_max = x
            elif x < x_min:
                x_min = x

            if y > y_max:
                y_max = y
            elif y < y_min:
                y_min = y

        for i in range(x_min, x_max + 1):
            for j in range(y_min, y_max + 1):
                cls.ground_tiles.append([i, j])

    @classmethod
    def set_resolution(cls, res):
        cls.resolution = res

    @classmethod
    def set_transVec(cls, vec):
        cls.translate_vec = vec

    @classmethod
    def get_surronded_tiles(self):
        for tile in self.ground_tiles + self.extended_tiles:
            tile1 = [tile[0] + 1, tile[1]]
            tile2 = [tile[0] - 1, tile[1]]
            tile3 = [tile[0], tile[1] - 1]
            tile4 = [tile[0], tile[1] + 1]
            tile5 = [tile[0] + 1, tile[1] + 1]
            tile6 = [tile[0] + 1, tile[1] - 1]
            tile7 = [tile[0] - 1, tile[1] + 1]
            tile8 = [tile[0] - 1, tile[1] - 1]
            for t in [tile1, tile2, tile3, tile4, tile5, tile6, tile7, tile8]:
                if not t in self.ground_tiles and not t in self.extended_tiles:
                    self.extended_tiles.append(t)

    def required_ground(self, x, y):
        tile = [x//1000, y//1000]
        tolerance = 0
        if not tile in self.ground_tiles:
            self.ground_tiles.append(tile)


    def getVertexData(self, filename, res):
        data = []
        if res == 'hd':
            r = 1
        else:
            r = 5
        z_trans = 8849
        x_trans = 0
        y_trans = 0

        with open(join('track', f'{filename}_parthed.igc'), 'r') as file:
            for i, line in enumerate(file):
                if i % r == 0:
                    x, y, z = (float(n) for n in line.split(' '))
                    self.required_ground(int(x), int(y))
                    if z < z_trans:
                        x_trans = x
                        y_trans = y
                        z_trans = z

                    data.append(np.array((x,y,z)))
        self.set_transVec(np.array((x_trans, y_trans, z_trans)))
        l = len(data)

        for i in range(l):
            data[i] -= self.translate_vec
            data[i] *= self.size_factor
            data[i] = data[i].tolist()

        return data

    def getVertexData_shadow(self, res):
        data = []
        if res == 'hd':
            r = 1
        else:
            r = 1
        for i in range(len(self.vertex[r])):
            if i % 3 == 0:
                x1,y1,z1 = self.vertex[r][i]
                x2,y2,z2 = x1,y1,0.
                data.append([(x1,y1,z1),(x2,y2,z2)])

        return data

    def render(self):
        glColor3fv(self.color)
        glBegin(GL_LINE_STRIP)
        for pts in self.vertex[self.resolution]:
            glVertex3fv(pts)
        glEnd()

        if self.resolution == 1:
            glBegin(GL_LINES)
            for quad in self.vertex_shadow[self.resolution]:
                glColor3fv(self.color)
                glVertex3fv(quad[0])
                glColor3fv((0, 0, 0))
                glVertex3fv(quad[1])
            glEnd()

class Topo:
    resolution = 1
    color = []

    def __init__(self, light_pos, TILES, size_factor):
        self.light_pos = light_pos
        self.hide = False
        self.size_factor = size_factor

        self.tiles = self.getTiles(TILES)
        self.triangleIDX = [self.get_triangleIDX(len(self.tiles[0][0]) - 1), self.get_triangleIDX(len(self.tiles[0][1]) - 1)]
        self.triangleColor = [self.getTriangleColor(0), self.getTriangleColor(1)]
    
    @classmethod
    def set_resolution(cls, res):
        cls.resolution = res
    
    def getTiles(self, tiles):
        data = []

        for tile in tiles:
            filename = f'SWISSALTI3D_2_XYZ_CHLV95_LN02_{str(tile[0])}_{str(tile[1])}.xyz'
            print(filename)

            try:
                vertex = [self.getVertexData(filename, 'ld'), self.getVertexData(filename, 'hd')]
                data.append(vertex)
            except FileNotFoundError:
                print("NOT FOUND")
                continue

        return data

    def getTriangleColor(self, res):
        data = []
        section = []
        for tile in self.tiles:

            for triIdx in self.triangleIDX[res]:
                
                x1, y1 = triIdx[0]
                x2, y2 = triIdx[1]
                x3, y3 = triIdx[2]
                #glColor3fv((1,0,0))
                section.append(self.get_color(tile, x1, y1, x2, y2, x3, y3))
            data.append(section)
            del section
            section = []
        return data


    def getVertexData(self, filename, res):
        data = []
        with open(join('alti_data', 'thirdlayer', f'{res}3', filename), 'r') as file:
            i = 0
            section = []
            checkVar = None
            xMin = 30000000
            yMin = 20000000
            zMin = 2000
            for line in file:
                x, y, z = (float(n) for n in line.split(' '))

                if xMin > x:
                    xMin = x
                if yMin > y:
                    yMin = y
                if zMin > z:
                    zMin = z

                if y != checkVar:
                    if checkVar == None:
                        checkVar = y
                    elif checkVar != None:
                        checkVar = y
                        data.append(section)
                        del section
                        section = []
                        i += 1
                section.append(np.array((x,y,z)))

        l = len(data)
        for i in range(l):
            for j in range(l):
                data[i][j] -= Track.translate_vec
                data[i][j] *= self.size_factor
                data[i][j] = data[i][j].tolist()

        return data

    def get_triangleIDX(self, l):
        idx = []
        idxTri = []
        line = []

        for i in range(l):
            del line
            line = []
            for j in range(l+1):
                line.append((i, j))
                line.append((i+1, j))
            idx.append(line)
        
        for liine in idx:
            for i in range(2 * l):
                idxTri.append((liine[i], liine[i+1], liine[i+2]))

        return idxTri

    def render(self):
        if self.hide:
            return
        i = 0
        for tile in self.tiles:
            j = 0
            glBegin(GL_TRIANGLES)

            for triIdx in self.triangleIDX[self.resolution]:
                x1, y1 = triIdx[0]
                x2, y2 = triIdx[1]
                x3, y3 = triIdx[2]
                glColor3fv(self.triangleColor[self.resolution][i][j])
                glVertex3fv(tile[self.resolution][x1][y1])
                glVertex3fv(tile[self.resolution][x2][y2])
                glVertex3fv(tile[self.resolution][x3][y3])
                j += 1

            glEnd()
            i += 1

    def get_color(self, tile, x1, y1, x2, y2, x3, y3):
        intensity = 1
        D = self.light_pos - tile[self.resolution][x1][y1]
        d = np.sqrt(np.dot(D, D))
        V1 = np.array(tile[self.resolution][x2][y2]) - np.array(tile[self.resolution][x1][y1])
        V2 = np.array(tile[self.resolution][x3][y3]) - np.array(tile[self.resolution][x1][y1])
        N = np.cross(V1, V2)

        if N[2] < 0: 
            N *= -1
        n = np.sqrt(np.dot(N, N))
        intensity = np.dot(N, D) / (n * d)

        return (self.color * intensity).tolist()