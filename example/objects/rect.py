import pygame
from pygame_engine import DynamicObject

class Rect(DynamicObject):
    
    def __init__(self, name, tag, visible, static, layer, position, scale, rotate, density, friction):
        super().__init__(name, tag, visible, static, layer, position, scale, rotate, density, friction)
        self.image = pygame.image.load("D:/pygame_engine/example/core.png")