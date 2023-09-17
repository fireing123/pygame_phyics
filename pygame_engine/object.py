import pygame
from typing import Dict
import pygame_engine
from Box2D import *
from Box2D.b2 import *
import pdb
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
        pygame_engine.scene.remove(self)

    @staticmethod
    def instantiate(object):
        pygame_engine.scene.add(object)

class GameObject(object):
    
    def __init__(self, name: str, tag, visible, static, layer):
        super().__init__(name, layer, tag)
        self.visible = visible
        self.static = static

                
class StaticObject(GameObject): 
    def __init__(self, name, tag, visible, static, layer,
        position, rotate, scale : tuple | float, shape_type):
        super().__init__(name, tag, visible, static, layer)
        match shape_type:
            case "chain":
                self.body.CreateChainFixture
            case "circle":
                self.shape = b2CircleShape()
            case "edge":
                self.body.CreateEdgeFixture
            case "polygon":
                self.shape = b2PolygonShape(box=scale)
        self.body : b2Body = pygame_engine.phyics_world.CreateStaticBody(
            position=position,
            angle=rotate,
            shapes=self.shape
            )
    
    def render(self, surface, camera):
        for fixture in self.body.fixtures:
            vertices = [(self.body.transform * v) * PPM for v in fixture.shape.vertices]
            vertices = [(v[0], surface.get_size()[1] - v[1]) for v in vertices]
            pygame.draw.polygon(surface, (127, 127, 127, 255), vertices, 1)


class DynamicObject(GameObject):
    def __init__(self, name, tag, visible, static, layer,
        position, rotate, scale : tuple | float, shape_type,
        density, friction):
        super().__init__(name, tag, visible, static, layer)
        self.body : b2Body = pygame_engine.phyics_world.CreateDynamicBody(
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
    
    def render(self, surface, camera):
        for fixture in self.body.fixtures:
            vertices = [(self.body.transform * v) * PPM for v in fixture.shape.vertices]
            vertices = [(v[0], surface.get_size()[1] - v[1]) for v in vertices]
            pygame.draw.polygon(surface, (127, 127, 127, 255), vertices, 1)
