from pygame.math import Vector2 as Vector
from pygame_phyics import PPM

class Parent:
    def __init__(self):
        self.position = Vector(0, 0)
        self.world_position = Vector(0, 0)
        self.rotation = 0
        self.world_rotation = 0
        self.children = []

    def set_world(self):
        for child in self.children:
            child.change_location()

class Location(Parent):
    def __init__(self, position: Vector, rotation: int):
        self.__position = position
        self.__rotation = rotation
        self.__world_position = Vector(0, 0)
        self.__world_rotation = 0
        self.parent : Parent = None
        self.children = []

    def set_parent(self, parent: Parent):
        self.parent = parent
        parent.children.append(self)
    
    @property
    def position(self):
        return self.__position.copy()
    
    @position.setter
    def position(self, vector):
        self.__position = vector
        self.change_location()

    @property
    def rotation(self):
        return self.__rotation
    
    @rotation.setter
    def rotation(self, degree):
        self.__rotation = degree
        self.change_location()
        
    @property
    def world_position(self):
        return self.__world_position
    
    @property
    def world_rotation(self):
        return self.__world_rotation
    
    def change_location(self):
        self.__world_position = self.parent.world_position + self.__position.rotate(self.parent.rotation)
        self.__world_rotation = self.parent.world_rotation + self.__rotation
        for child in self.children:
            child.change_location()

  
class PhysicsLocation:
    def __init__(self, physics):
        self.physics = physics
    
    def set_parent(self, parent: Parent):
        self.parent = parent
    
    @property
    def position(self):
        return self.world_position - self.parent.world_position
    
    @position.setter
    def position(self, value: Vector):
        self.world_position = self.parent.world_position + value
        self.change_location()
    
    @property
    def rotation(self):
        return self.world_rotation - self.parent.world_rotation
    
    @rotation.setter
    def rotation(self, angle: int):
        self.world_rotation = self.parent.world_rotation + angle
        self.change_location()
        
    @property
    def world_position(self):
        return Vector(self.physics.body.transform.position.x, self.physics.body.transform.position.y) * PPM
    
    @world_position.setter
    def world_position(self, vector: Vector):
        self.physics.body.transform.position.x = vector.x / PPM
        self.physics.body.transform.position.y = vector.y / PPM
    
    @property
    def world_rotation(self):
        return self.physics.body.angle
    
    @world_rotation.setter
    def world_rotation(self, rotation: int):
        self.physics.body.angle = rotation
    
    def set_location(self, location: Location):
        self.parent = location.parent
        self.children = location.children
        self.position = location.position
        self.rotation = location.rotation

    def change_location(self):
        self.world_position = self.parent.world_position + self.position.rotate(self.parent.rotation)
        self.world_rotation = self.parent.world_rotation + self.rotation
        for child in self.children:
            child.change_location()