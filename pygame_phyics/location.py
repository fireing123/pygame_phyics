from pygame_phyics.vector import Vector
from pygame_phyics.util import getter
from pygame_phyics import PPM

class Parent:
    def __init__(self):
        self.position = Vector(0, 0)
        self.world_position = Vector(0, 0)
        self.rotation = 0
        self.world_rotation = 0
        self.children = []

class Location(Parent):
    def __init__(self, position: Vector, rotation: int):
        self.position = position
        self.rotation = rotation
        

    def set_parent(self, parent: Parent):
        self.parent = parent
        parent.child = self
        
        
    @getter
    def world_position(self):
        return self.parent.world_position + self.position
    
    @getter
    def world_rotation(self):
        return self.parent.world_rotation + self.rotation
    
class PhysicsLocation:
    def __init__(self, physics):
        self.physics = physics
        self.children = []
    
    def set_parent(self, parent: Parent):
        self.parent = parent
    
    @property
    def position(self):
        parent = Vector(self.parent.world_position.x, self.parent.world_position.y)
        world_pos = Vector(self.physics.body.transform.position.x * PPM, self.physics.body.transform.position.y * PPM)
        return world_pos - parent
    
    @position.setter
    def position(self, value: Vector):
        self.physics.body.transform.position.x = self.parent.position.x + value.x / PPM
        self.physics.body.transform.position.y = self.parent.position.y + value.y / PPM
    
    @property
    def rotation(self):
        parent = self.parent.rotation
        return self.physics.angle - parent
    
    @getter
    def world_position(self):
        return Vector(self.physics.body.transform.position.x, self.physics.body.transform.position.y)
    
    @getter
    def world_rotation(self):
        return self.physics.body.angle