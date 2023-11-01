import math
from pygame_phyics.util import const

class Vector:
    def __init__(self, x: float, y:float):
        self.x = x
        self.y = y
        self.index = 0
    
    def __getitem__(self, index):
        match index:
            case 0:
                return self.x
            case 1:
                return self.y

    def isiter():pass

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index < 2:
            item = (self.x, self.y)[self.index]
            self.index += 1
            return item
        else:
            self.index = 0
            raise StopIteration
    
    
    @const
    def xy(self):
        return self.x, self.y
    
    @const
    def empty(self):
        return Vector(0, 0)
    
    def rotate_vector(self, vector, angle):
        angle_radians = math.radians(360 - angle)
        x_a, y_a = self.xy
        x_b, y_b = vector.xy
        x = (x_b - x_a) * math.cos(angle_radians) - (y_b - y_a) * math.sin(angle_radians) + x_a
        y = (x_b - x_a) * math.sin(angle_radians) + (y_b - y_a) * math.cos(angle_radians) + y_a
        return Vector(x, y)
    
    def add_vector(self, vector):
        x= self.x + vector.x
        y= self.y + vector.y
        return Vector(x,y) 
    
    def sub_vector(self, vector):
        x= self.x - vector.x
        y= self.y - vector.y
        return Vector(x,y) 
        
    def div_vector(self, vector):
        x= self.x / vector.x
        y= self.y / vector.y
        return Vector(x,y) 
        
    def mul_vector(self, vector):
        x= self.x * vector.x
        y= self.y * vector.y
        return Vector(x,y) 
    
    def add_float(self, float):
        x= self.x + float
        y= self.y + float
        return Vector(x,y) 
        
    def sub_float(self, float):
        x= self.x - float
        y= self.y - float
        return Vector(x,y) 
        
    def div_float(self, float):
        x= self.x / float
        y= self.y / float
        return Vector(x,y) 
    
    def mul_float(self, float):
        x= self.x * float
        y= self.y * float
        return Vector(x,y) 
        
    def __add__(self, value):
        if type(value) == Vector:
            return self.add_vector(value)
        elif type(value) in [int, float]:
            return self.add_float(value)
        else:
            raise TypeError(f"{type(value)} 는 알맞은 타입이 아닙니다 Vector or float/int")
    
    def __sub__(self, value):
        if type(value) == Vector:
            return self.sub_vector(value)
        elif type(value) in [int, float]:
            return self.sub_float(value)
        else:
            raise TypeError(f"{type(value)} 는 알맞은 타입이 아닙니다 Vector or float/int")
    
    def __div__(self, value):
        if type(value) == Vector:
            return self.div_vector(value)
        elif type(value) in [int, float]:
            return self.div_float(value)
        else:
            raise TypeError(f"{type(value)} 는 알맞은 타입이 아닙니다 Vector or float/int")
    
    def __mul__(self, value):
        if type(value) == Vector:
            return self.mul_vector(value)
        elif type(value) in [int, float]:
            return self.mul_float(value)
        else:
            raise TypeError(f"{type(value)} 는 알맞은 타입이 아닙니다 Vector or float/int")