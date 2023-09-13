import pygame
from typing import Dict
from pygame_engine import scene

class Component:
    def update(self): pass
    def render(self, surface: pygame.Surface, camera: tuple): pass
    def delete(self): pass

class object(pygame.sprite.Sprite, Component):
    
    def __init__(self, name, layer):
        self.name = name
        self.__layer = layer

    @property
    def layer(self):
        """
        object layer
        """
        return self.__layer

class GameObject(object):
    
    def __init__(self, name: str, position=(0,0), layer=3):
        super().__init__(name, layer)
        scene.add(self)
        self.image: pygame.Surface
        self.rect: pygame.Rect
        self.__position = pygame.Vector2(*position)
        self.visible = True
    
    def delete(self):
        for group in self.groups():
            group.remove(self)
        scene.remove(self)
    
    @staticmethod
    def instantiate(json: Dict):
        pass
    
    @property
    def position(self):
        return self.__position
    
    @position.setter
    def position(self, value: tuple):
        self.__position = value
        self.rect.center = value