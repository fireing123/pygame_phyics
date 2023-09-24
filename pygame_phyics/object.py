import math
import pygame
from typing import Dict
from pygame_phyics import Game
from pygame_phyics import PPM
from Box2D import *
from Box2D.b2 import *

def rotate_point_around_origin(x, y, angle_degrees):
    angle_radians = math.radians(angle_degrees)
    new_x = x * math.cos(angle_radians) - y * math.sin(angle_radians)
    new_y = x * math.sin(angle_radians) + y * math.cos(angle_radians)
    return new_x, new_y

def rotate_point_b_around_a(a, b, angle_degrees):
    b_relative_to_a = (b[0] - a[0], b[1] - a[1])
    rotated_b_relative_to_a = rotate_point_around_origin(b_relative_to_a[0], b_relative_to_a[1], angle_degrees)
    rotated_b = (rotated_b_relative_to_a[0] + a[0], rotated_b_relative_to_a[1] + a[1])
    return rotated_b

class Component:
    def update(self):
        pass
    def render(self, surface, camera):
        pass
    
class ImageObject(Component):
    def __init__(self, object, image, position, angle):
        self.object = object
        self.og_image = pygame.image.load(image)
        self.image = self.og_image
        self.rect = self.image.get_rect()
        self.position = position
        self.angle = angle
    
    def update(self):
        position = rotate_point_b_around_a(self.object.position * PPM, self.object.position * PPM + self.position, self.object.angle)
        self.image = pygame.transform.rotate(self.og_image, self.angle + self.object.angle)
        self.rect = self.image.get_rect(center=position)

    def render(self, surface, camera):
        self.rect.centery = surface.get_size()[1] - self.rect.centery
        self.rect.center = self.rect.center[0] - camera.x, self.rect.center[1] - camera.y
        surface.blit(self.image, self.rect)

class Joint:
    joints = []
    
    def CreateJoint(self, frequency_hz, damping_ratio, body, localAnchor_a, localAnchor_b):
        joint = b2DistanceJointDef(
            frequencyHz=frequency_hz,
            dampingRatio=damping_ratio,
            bodyA=self.body,
            bodyB=body,
            localAnchorA=localAnchor_a,
            localAnchorB=localAnchor_b
        )
        created_joint = Game.phyics_world.CreateJoint(joint)
        Joint.joints.append(created_joint)
        return created_joint

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
    
    def __init__(self, name: str, tag, visible, layer):
        super().__init__(name, layer, tag)
        self.visible = visible
    
def circle_render(circle, body, surface, camera):
    position = body.transform * circle.pos * PPM
    position = (position[0] - camera[0], surface.get_size()[1] - position[1] - camera[1])
    pygame.draw.circle(surface, (127, 127, 127, 255), [int(
        x) for x in position], int(circle.radius * PPM), 1)
b2CircleShape.render = circle_render

def polygon_render(polygon, body, surface, camera):
    vertices = [(body.transform * v) * PPM for v in polygon.vertices]
    vertices = [(v[0], surface.get_size()[1] - v[1]) for v in vertices]
    vertices = [(v[0] - camera[0], v[1] - camera[1]) for v in vertices]
    pygame.draw.polygon(surface, (127, 127, 127, 255), vertices, 1)
b2PolygonShape.render = polygon_render
    
class Phyics(GameObject, Joint):

    def delete(self):
        Game.phyics_world.DestroyBody(self.body)
        GameObject.delete(self)
    
    @property
    def position(self):
        return self.body.transform.position
    
    @position.getter
    def position(self):
        return self.body.transform.position
    
    @position.setter
    def position(self, value):
        self.body.transform.position
    
    @property
    def angle(self):
        return self.body.angle
    
    @angle.getter
    def angle(self):
        return self.body.angle * 45
    
    @angle.setter
    def angle(self, value):
        self.body.angle / 45
          
class StaticObject(Phyics): 
    def __init__(self, name, tag, visible, layer,
        position, rotate, scale : tuple | float, shape_type, collid_visible):
        super().__init__(name, tag, visible, layer)
        self.collid_visible = collid_visible
        match shape_type:
            case "chain":
                self.shape = b2ChainShape()
            case "circle":
                self.shape = b2CircleShape()
            case "edge":
                self.shape = b2EdgeShape(vertices=scale)
            case "polygon":
                self.shape = b2PolygonShape(vertices=scale)
        self.body : b2Body = Game.phyics_world.CreateStaticBody(
            position=position,
            angle=rotate,
            shapes=self.shape
            )
    
    def render(self, surface, camera):
        if self.collid_visible:
            for fixture in self.body.fixtures:
                fixture.shape.render(self.body, surface, camera)

class DynamicObject(Phyics):
    def __init__(self, name, tag, visible, layer,
        position, rotate, scale : tuple | float, shape_type, collid_visible,
        density, friction):
        super().__init__(name, tag, visible, layer)
        self.collid_visible = collid_visible
        self.body : b2Body = Game.phyics_world.CreateDynamicBody(
            position=position,
            angle=rotate
        )
        match shape_type:
            case "chain":
                pass
            case "circle":
                self.shape = self.body.CreateCircleFixture(radius=scale, density=density, friction=friction)
            case "edge":
                pass
            case "polygon":
                self.fixture = self.body.CreatePolygonFixture(vertices=scale, density=density, friction=friction)
    
    def render(self, surface, camera):
        if self.collid_visible:
            for fixture in self.body.fixtures:
                fixture.shape.render(self.body, surface, camera)
        