import pygame
from pygame_engine.instantiate import import_classes, load
from pygame_engine.scene import Scene
from pygame_engine.object import GameObject

screen : pygame.Surface
scene: Scene
is_running = True
clock = pygame.time.Clock()
class_list = {}

def init(size, title, class_dir):
    global screen
    load_class(class_dir)
    pygame.init()
    pygame.display.set_caption(title)
    screen = pygame.display.set_mode(size)

def set_scene(new_scene):
    global scene
    scene.clear()
    scene = new_scene

def load_class(dir_path):
    global class_list
    class_list = import_classes(dir_path)

def world(world_path):
    def real_world(func):
        def wrapper():
            global scene
            scene.darkening()
            scene = Scene.load()
            load(world_path)
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
        
        scene.update()
        scene.render()