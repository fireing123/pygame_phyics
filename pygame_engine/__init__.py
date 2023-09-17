import pygame
from Box2D import *
from Box2D.b2 import *

from pygame_engine.object import GameObject
from pygame_engine.instantiate import import_classes, load
from pygame_engine.scene import Scene

from pygame_engine.object import StaticObject
from pygame_engine.object import DynamicObject

camera : tuple
screen : pygame.Surface
scene: Scene
is_running = True
clock = pygame.time.Clock()
class_list = {}
phyics_world : b2World
time_step = 1 / 60
ve_iters = 10
pos_iters = 10

def init(size, title, class_dir):
    global screen
    global scene
    global phyics_world
    load_class(class_dir)
    pygame.init()
    pygame.display.set_caption(title)
    screen = pygame.display.set_mode(size)
    phyics_world = b2World()
    scene = Scene.load()
    

def load_class(dir_path):
    global class_list
    class_list = import_classes(dir_path)

def world(world_path):
    def real_world(func):
        def wrapper():
            global scene
            scene.darkening()
            global phyics_world
            phyics_world = b2World()
            scene = Scene.load()
            load(world_path, class_list)
            scene.brightening()
            func()
            scene.layers.clear()
        return wrapper
    return real_world
            

def game_loop(events=[], funcs=[]):
    global is_running
    while is_running:
        clock.tick(60)
        for func in funcs:
            func()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            for event_func in events:
                event_func(event)
        
        phyics_world.Step(time_step, ve_iters, pos_iters)
        scene.update()
        scene.render(screen)
        pygame.display.update()