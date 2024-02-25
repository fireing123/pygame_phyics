import pygame
from pygame_phyics import game
from pygame_phyics import Game
from pygame_phyics.vector import Vector


Game.init((500, 400), "TileMap")

#Game.import_objects("objects/")

@game.world("scene/tilemap.json")
def tilemap():

    def start(cls):
        pass

    def event(cls, event):
        pass 

    def update(cls):
        pass
    return start, event, update



tilemap()