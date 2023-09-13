from typing import List
import pygame_engine

class Camera:
    def __init__(self):
        self.__x = 0
        self.__y = 0
        
    def __get__(self):
        return (self.x, self.y)
    
    def __set__(self, value):
        self.x, self.y = value
    
    @property
    def x(self):
        return self.__x
    
    @x.getter
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value
    
    @property
    def y(self):
        return self.__y
    
    @y.getter
    def y(self):
        return self.__y
    
    @y.setter
    def y(self, value):
        self.__y = value

class Scene:
    
    def __init__(self, camera):
        self.camera = camera
        self.layers = [[],[],[],[],[],[],[],[]]
    
    def layer_loop(self, method, *args):
        for layer in self.layers:
            for obj in layer:
                func = getattr(obj, method)
                func(*args)
    
    def update(self):
        self.layer_loop("update")
    
    def render(self, surface):
        self.layer_loop("render", surface, self.camera)
    
    def add(self, obj):
        layer = self.layers[obj.layer]
        layer.append(obj)
    
    def absorb(self, list : List):
        for obj in list:
            self.add(obj)
    
    def remove(self, obj):
        try:
            self.layers[obj.layer].remove(obj)
        except ValueError:
            print('value error')
            
    def clear(self):
        for layer in self.layers:
            for _ in range(len(layer)):
                layer[0].delete()
         
    def darkening(self):
        pass
    
    def brightening(self):
        pass
    
    @staticmethod
    def load():
        camera = Camera()
        pygame_engine.set_scene(Scene(camera))