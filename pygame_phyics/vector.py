from collections.abc import Callable
import math
from typing import Any
from pygame_phyics.error import ImmutableAttributeError
from multipledispatch import dispatch

class const(property):
    def setter(self):
        raise ImmutableAttributeError(Vector, "???")

class Vector:
    def __init__(self, x: float, y:float):
        self.x = x
        self.y = y
        self.index = 0
    
    def isiter(): pass
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index < 2:
            item = (self.x, self.y)[self.index]
            self.index += 1
            return item
        else:
            raise StopIteration
    
    
    @const
    def xy(self):
        return self.x, self.y
    
    @xy.getter
    def xy(self):
        return self.x, self.y
    
    @const
    def empty(self):
        return Vector(0, 0)
    
    @empty.getter
    def empty(self):
        return Vector(0, 0)

    def rotate_vector(self, vector, angle):
        angle_radians = math.radians(360 - angle)
        x_a, y_a = self.xy
        x_b, y_b = vector.xy
        x = (x_b - x_a) * math.cos(angle_radians) - (y_b - y_a) * math.sin(angle_radians) + x_a
        y = (x_b - x_a) * math.sin(angle_radians) + (y_b - y_a) * math.cos(angle_radians) + y_a
        return x, y
    
    def add_vector(self, vector):
        self.x += vector.x
        self.y += vector.y
    
    def sub_vector(self, vector):
        self.x -= vector.x
        self.y -= vector.y
        
    def div_vector(self, vector):
        self.x /= vector.x
        self.y /= vector.y
        
    def mul_vector(self, vector):
        self.x *= vector.x
        self.y *= vector.y
    
    def add_float(self, float):
        self.x += float
        self.y += float
        
    def sub_float(self, float):
        self.x -= float
        self.y -= float
        
    def div_float(self, float):
        self.x /= float
        self.y /= float
    
    def mul_float(self, float):
        self.x *= float
        self.y *= float
        
    def __add__(self, value):
        if type(value) == Vector:
            self.add_vector(value)
        elif type(value) in [int, float]:
            self.add_float(value)
        else:
            raise TypeError(f"{type(value)} 는 알맞은 타입이 아닙니다 Vector or float/int")
    
    def __sub__(self, value):
        if type(value) == Vector:
            self.sub_vector(value)
        elif type(value) in [int, float]:
            self.sub_float(value)
        else:
            raise TypeError(f"{type(value)} 는 알맞은 타입이 아닙니다 Vector or float/int")
    
    def __div__(self, value):
        if type(value) == Vector:
            self.div_vector(value)
        elif type(value) in [int, float]:
            self.div_float(value)
        else:
            raise TypeError(f"{type(value)} 는 알맞은 타입이 아닙니다 Vector or float/int")
    
    def __mul__(self, value):
        if type(value) == Vector:
            self.mul_vector(value)
        elif type(value) in [int, float]:
            self.mul_float(value)
        else:
            raise TypeError(f"{type(value)} 는 알맞은 타입이 아닙니다 Vector or float/int")