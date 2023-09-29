import pygame
from pygame.mouse import *
from pygame_phyics import Game

def mouse_event():
    for layer in Game.scene.layers[::-1]:
        for obj in layer:
            if obj.rect != None:
                if obj.rect.collidepoint(get_pos()):
                    if obj.collide == 'out':
                        obj.collide = 'in'
                        obj.on_mouse_enter(get_pos())
                    elif obj.collide == 'in':
                        obj.on_mouse_stay(get_pos())
                elif obj.collide == 'in':
                    obj.collide = 'out'
                    obj.on_mouse_exit(get_pos())
