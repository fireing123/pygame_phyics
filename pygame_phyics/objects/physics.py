import pygame
import Box2D
from pygame_phyics import PPM
from pygame_phyics.manger import Manger
from pygame_phyics.objects.gameobject import GameObject
from pygame_phyics.objects.component import Component
from pygame_phyics.objects.joint import Joint
from pygame_phyics.location import PhysicsLocation
from pygame_phyics.collison import Collison

def circle_render(circle, body, surface, camera):
    position = body.transform * circle.pos * PPM
    position = camera((position[0], Manger.HEIGHT - position[1]))
    pygame.draw.circle(surface, (0, 0, 0, 255), [int(
        x) for x in position], int(circle.radius * PPM), 1)
Box2D.b2CircleShape.render = circle_render
def polygon_render(polygon, body, surface, camera):
    vertices = [(body.transform * v) * PPM for v in polygon.vertices]
    vertices = [(v[0], Manger.HEIGHT - v[1]) for v in vertices]
    vertices = [camera(v) for v in vertices]
    pygame.draw.polygon(surface, (0, 0, 0, 255), vertices, 1)
Box2D.b2PolygonShape.render = polygon_render

class Physics(Component, Joint):
    """물리오브젝트 컴포넌트 (오브젝트가 아님!)"""
    phyics_arr = []

    def __init__(self, object, **kwargs):
        Physics.phyics_arr.append(self)
        self.object: GameObject = object
        self.collide_visible = kwargs.get('visible', False)
        self.collide_enter: dict[Physics, str] = {}

        match kwargs["bodyType"]:
            case "static":
                self.body : Box2D.b2Body = Manger.world.CreateStaticBody()
            case "dynamic":
                self.body : Box2D.b2Body = Manger.world.CreateDynamicBody()
            case _:
                raise ValueError("bodyType [static/dynamic] only")
        self.body.userData = self
        match kwargs["shapeType"]:
            case "chain":
                self.fixture = self.body.CreateChainFixture(vertices_chain=kwargs["scale"], density=kwargs.get("density", 0), friction=kwargs.get("friction", 0)) # 지원하지 않음 -> 테두리 렌더
            case "circle":
                self.fixture = self.body.CreateCircleFixture(radius=kwargs["scale"], density=kwargs.get("density", 0), friction=kwargs.get("friction", 0))
            case "edge":
                self.fixture = self.body.CreateEdgeFixture(vertices=kwargs["scale"], density=kwargs.get("density", 0), friction=kwargs.get("friction", 0)) # 지원하지않음 -> 테두리 렌더
            case "polygon":
                self.fixture = self.body.CreatePolygonFixture(vertices=kwargs["scale"], density=kwargs.get("density", 0), friction=kwargs.get("friction", 0))

    def set_location(self):
        phy_loc = PhysicsLocation(self)
        phy_loc.set_location(self.object.location)
        self.object.location = phy_loc

    def collision(self):
        for phyics, status in list(self.collide_enter.items()):
            collison = Collison(
                phyics.object,
                phyics,
                self.object,
                self
            )

            if status == 'enter':
                self.object.on_collision_enter(collison)
                self.collide_enter[phyics] = 'stay'
            elif status == 'stay':
                self.object.on_collision_stay(collison)
            elif status == 'exit':
                self.object.on_collision_exit(collison)
                del self.collide_enter[phyics]
            else:
                raise KeyError("status :", status)
    
    def render(self, surface, camera):
        if self.collide_visible:
            for fixture in self.body.fixtures:
                fixture.shape.render(self.body, surface, camera)
    
    def delete(self):
        """이 오브젝트를 물리 새상과 씬에서 제거합니다"""
        Physics.phyics_arr.remove(self)
        Manger.world.DestroyBody(self.body)

class StaticObject(GameObject):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name, scale, shape, collid_visible):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        self.phyics = Physics(self, scale=scale, shapeType=shape, bodyType="static", visible=collid_visible)
        self.components.append(self.phyics)
    
    def instantiate(self):
        super().instantiate()
        self.phyics.set_location()

class DynamicObject(GameObject):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name, scale, shape, collid_visible, density, friction):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        self.phyics = Physics(self, scale=scale, shapeType=shape, bodyType="dynamic", visible=collid_visible, density=density, friction=friction)
        self.components.append(self.phyics)
    
    def instantiate(self):
        super().instantiate()
        self.phyics.set_location()