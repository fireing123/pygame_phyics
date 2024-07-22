import pygame
import Box2D
from pygame_phyics import PPM
from pygame_phyics.location import PhysicsLocation
from pygame_phyics.manger import Manger
from pygame_phyics.objects.gameobject import GameObject
from pygame_phyics.objects.joint import Joint
from pygame_phyics.collison import Collison

class Physics(GameObject, Joint):
    """물리오브젝트에 공통점"""
    
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        GameObject.__init__(self, name, layer, tag, visible, position, rotation, parent_name)
        self.collide_enter = []
        self.bpos = self.location.position
        self.brot = self.location.rotation
        self.location = PhysicsLocation(self)
        
    def set_location(self):
        self.location.position = self.bpos
        self.location.rotation = self.brot
        del self.bpos
        del self.brot
    
    def on_collision_enter(self, collision: Collison):
        """물리 오브젝트가 충돌시 이 함수가 호출됩니다

        Args:
            collision (GameObject): 충돌하는 상대 오브젝트 입니다
        """
        pass
    
    def clean_collision(self):
        """충돌하고 상대 오브젝트 주소를 삭제해 다음 충돌을 받을수 있도록 합니다"""
        self.collide_enter.clear()
    
    def render(self, surface, camera):
        if self.collide_visible:
            for fixture in self.body.fixtures:
                fixture.shape.render(self.body, surface, camera)
    
    def delete(self):
        """이 오브젝트를 물리 새상과 씬에서 제거합니다"""
        Manger.world.DestroyBody(self.body)
        GameObject.delete(self)
        
        
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

class StaticObject(Physics): 
    """정적 물리 오브젝트"""
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name, scale, shape_type, collide_visible):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        self.collide_visible = collide_visible
        match shape_type:
            case "chain":
                self.shape = Box2D.b2ChainShape(vertices_chain=scale)
            case "circle":
                self.shape = Box2D.b2CircleShape(radius=scale)
            case "edge":
                self.shape = Box2D.b2EdgeShape(vertices=scale)
            case "polygon":
                self.shape = Box2D.b2PolygonShape(vertices=scale)
        self.body : Box2D.b2Body = Manger.world.CreateStaticBody(
            shapes=self.shape
            )
        self.body.userData = self


class DynamicObject(Physics):
    """동적 물리 오브젝트"""
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name, scale : tuple | float, shape_type, collide_visible,
        density, friction):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        self.collide_visible = collide_visible
        self.body : Box2D.b2Body = Manger.world.CreateDynamicBody()
        self.body.userData = self
        match shape_type:
            case "chain":
                self.shape = self.body.CreateChainFixture(vertices_chain=scale, density=density, friction=friction)
            case "circle":
                self.shape = self.body.CreateCircleFixture(radius=scale, density=density, friction=friction)
            case "edge":
                self.shape = self.body.CreateEdgeFixture(vertices=scale, density=density, friction=friction)
            case "polygon":
                self.fixture = self.body.CreatePolygonFixture(vertices=scale, density=density, friction=friction)