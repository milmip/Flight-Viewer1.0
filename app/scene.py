from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import pygame as pg
from model import *
from parth import FlightData
import os
from model import Topo

class Scene:
    def __init__(self, APP, config_data):
        self.app = APP

        self.scale = config_data['scale']

        self.minimap = Minimap(self.app, self.scale)
        self.help = Help(self.app)

        os.system("clear")
        print("HI, welcome in Flight Viewer 1.0\n")

        self.flight_data = FlightData(self)
        self.flight_data.parth_new_files()

        Track.color = (np.array(config_data['track_col'])/255).tolist()
        self.tracks = [Track(f, self.scale) for f in self.flight_data.input_files]
        Track.get_surronded_tiles()

        print("\nRecolting topography data...")
        print("Loading...")

        Topo.color = np.array(config_data['topo_col'])/255

        self.topos = [Topo(self.app.light_position, tiles, self.scale) 
                        for tiles in [Track.ground_tiles, Track.extended_tiles]]
        self.topos[1].hide = True

        print(f"{len(Track.ground_tiles) + len(Track.extended_tiles)} km^2 loaded !")

    def render(self):
        for topo in self.topos:
            topo.render()

        if Topo.resolution == 1:
            self.app.freeze = True
        
        for track in self.tracks:
            track.render()
            
        self.help.render()
        self.minimap.render()
    
    def update(self, key):
        if key == pg.K_v:
            self.topos[1].hide = not self.topos[1].hide
            self.app.freeze = False
        if key == pg.K_c:
            self.minimap.hide = not self.minimap.hide
            self.app.freeze = False
        if key == pg.K_q:
            self.minimap.set_zoom(1)
            self.app.freeze = False
        if key == pg.K_e:
            self.minimap.set_zoom(-1)
            self.app.freeze = False
        if key == pg.K_h:
            self.help.hide = not self.help.hide
            self.app.freeze = False
