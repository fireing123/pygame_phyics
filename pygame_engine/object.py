import pygame
from typing import Dict
from pygame_engine import Game

from Box2D import *
from Box2D.b2 import *

PPM = 20
STEP = 1.0/60

class Component:
    def update(self):
        pass
    def render(self, surface, camera):
        pass

class object(Component):
    
    def __init__(self, name, layer, tag):
        self.name = name
        self.tag = tag
        self.layer = layer

    def delete(self): 
        Game.scene.remove(self)

    @staticmethod
    def instantiate(object):
        Game.scene.add(object)

class GameObject(object):
    
    def __init__(self, name: str, tag, visible, static, layer):
        super().__init__(name, layer, tag)
        self.visible = visible
        self.static = static
        
def polygon_render(polygon, body, surface):
            vertices = [(body.transform * v) * PPM for v in polygon.vertices]
            vertices = [(v[0], surface.get_size()[1] - v[1]) for v in vertices]
            pygame.draw.polygon(surface, (127, 127, 127, 255), vertices, 1)
b2PolygonShape.render = polygon_render
                
class StaticObject(GameObject): 
    def __init__(self, name, tag, visible, static, layer,
        position, rotate, scale : tuple | float, shape_type):
        super().__init__(name, tag, visible, static, layer)
        match shape_type:
            case "chain":
                self.shape = b2ChainShape()
            case "circle":
                self.shape = b2CircleShape()
            case "edge":
                self.shape = b2EdgeShape()
            case "polygon":
                self.shape = b2PolygonShape(box=scale)
        self.body : b2Body = Game.phyics_world.CreateStaticBody(
            position=position,
            angle=rotate,
            shapes=self.shape
            )
    
    @property
    def position(self):
        return self.body.position
    
    def render(self, surface, camera):
        for fixture in self.body.fixtures:
            fixture.shape.render(self.body, surface)

class DynamicObject(GameObject):
    def __init__(self, name, tag, visible, static, layer,
        position, rotate, scale : tuple | float, shape_type,
        density, friction):
        super().__init__(name, tag, visible, static, layer)
        self.body : b2Body = Game.phyics_world.CreateDynamicBody(
            position=position,
            angle=rotate
        )
        match shape_type:
            case "chain":
                self.body.CreateChainFixture
            case "circle":
                self.shape = b2CircleShape()
            case "edge":
                self.body.CreateEdgeFixture
            case "polygon":
                self.fixture = self.body.CreatePolygonFixture(box=scale, density=density, friction=friction)
    
    @property
    def position(self):
        return self.body.position
    
    def render(self, surface, camera):
        for fixture in self.body.fixtures:
            fixture.shape.render(self.body, surface)