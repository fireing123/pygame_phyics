import pygame
from pygame_phyics import DynamicObject
from pygame_phyics import StaticObject
from pygame_phyics.object import ImageObject

class Rect(DynamicObject):
    def __init__(self, name, tag, visible, layer, position, rotate, scale: tuple | float, shape_type, collid_visible, density, friction):
        super().__init__(name, tag, visible, layer, position, rotate, scale, shape_type, collid_visible, density, friction)
        self.image = ImageObject(self, "./example/core.png", (0, 50), 45)

    def update(self):
        self.image.update()

    def render(self, surface, camera):
        super().render(surface, camera)
        self.image.render(surface, camera)

class Ground(StaticObject):
    pass