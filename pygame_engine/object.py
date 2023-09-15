import pygame
from typing import Dict
import pygame_engine
from Box2D import *
from Box2D.b2 import *

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

                
class MoveObject(GameObject): 
    def __init__(self, name, tag, visible, static, layer,
        position, rotate):
        GameObject.__init__(self, name, tag, visible, static, layer)
        self.def_body = b2BodyDef()
        self.def_body.position.Set(*position)
        self.def_body.angle = rotate
        self.body : b2Body = pygame_engine.phyics_world.CreateBody(self.def_body)

    def render(self, surface, camera):
        if not self.visible: return
        image = pygame.transform.rotate(self.image, self.body.angle)
        cx, cy = camera
        rx, ry = image.get_rect(center=(self.body.position.x, self.body.position.y)).topleft
        self.rect_position = rx - cx, ry - cy
        surface.blit(image, self.rect_position)

class StaticObject(MoveObject):
    def __init__(self, name, tag, visible, static, layer, position, scale, rotate):
        super().__init__(name, tag, visible, static, layer, position, rotate)
        self.shape = b2PolygonShape()
        self.shape.SetAsBox(*scale)
        self.body.CreateFixture(shape=self.shape)

class DynamicObject(MoveObject):
    def __init__(self, name, tag, visible, static, layer, position, scale, rotate,
        density, friction):
        super().__init__(name, tag, visible, static, layer, position, rotate)
        self.shape = b2PolygonShape()
        self.shape.SetAsBox(*scale)
        self.def_fixture = b2FixtureDef()
        self.def_fixture.shape = self.shape
        self.def_fixture.density = density
        self.def_fixture.friction = friction
        self.body.CreateFixture(self.def_fixture)