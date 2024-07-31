import pygame
import os
from pygame_phyics import *
from pygame_phyics import game

os.chdir(
    os.path.abspath(os.path.dirname(__file__))
)

SCREEN_SIZE = (1200, 800)
TITLE = "title"

Game.init(SCREEN_SIZE, TITLE)


#Game.import_objects("objects/", debug="log")

@game.world("main.json")
def main():

    def start(cls: Game):
        pass

    def event(cls: Game, event: pygame.event.Event):
        pass

    def update(cls: Game):
        pass
    return start, event, update

main()

