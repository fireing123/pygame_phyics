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
    
    def __init__(self, object, **kwargs):
        self.object: GameObject = object
        self.collide_visible = kwargs.get("collide_visible", False)
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

        self.object.location = PhysicsLocation(self, self.object.location.position, self.object.location.rotation)
    


    def collision(self):
        for phyics, status in list(self.collide_enter.items()):
            collison = Collison(
                self.object,
                self,
                phyics.object,
                phyics
            )

            if status == 'enter':
                self.object.on_collison_enter(collison)
                self.collide_enter[phyics] = 'stay'
            elif status == 'stay':
                self.object.on_collison_stay(collison)
            elif status == 'exit':
                self.object.on_collison_exit(collison)
                del self.collide_enter[phyics]
            else:
                raise KeyError("status :", status)
    
    def render(self, surface, camera):
        if self.collide_visible:
            for fixture in self.body.fixtures:
                fixture.shape.render(self.body, surface, camera)
    
    def delete(self):
        """이 오브젝트를 물리 새상과 씬에서 제거합니다"""
        Manger.world.DestroyBody(self.body)

class StaticObject(GameObject):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name, scale, shape, collide_visible):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        self.phyics = Physics(self, collide_visible=collide_visible, scale=scale, shapeType=shape, bodyType="static")

class DynamicObject(GameObject):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name, scale, shape, collide_visible, density, friction):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        self.phyics = Physics(self, collide_visible=collide_visible, scale=scale, shapeType=shape, bodyType="dynamic", density=density, friction=friction)