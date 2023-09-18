import pygame
from pygame import display

from Box2D import b2World

from pygame_engine.scene import Scene
from pygame_engine.instantiate import import_classes
from pygame_engine.instantiate import load as instantiate_load

def world(world_path):
    def real_world(func):
        def wrapper():
            Game.scene.darkening()
            Game.phyics_world = b2World()
            Game.scene = Scene()
            instantiate_load(world_path, Game.objs)
            Game.scene.brightening()
            func()
            del Game.scene
        return wrapper
    return real_world

class Game:
    
    is_running = True
    clock = pygame.time.Clock()
    time_step = 1 / 60
    ve_iters = 10
    pos_iters = 10
    objs = {}
    
    @classmethod
    def init(cls, size, title):
        pygame.init()
        display.set_caption(title)
        cls.screen = display.set_mode(size)
        cls.phyics_world = b2World()
        cls.scene = Scene()
    
    @classmethod
    def import_objects(cls, obj_dir):
        cls.objs.update(import_classes(obj_dir))
        
    @classmethod
    def loop(cls, events=[], funcs=[]):
        while cls.is_running:
            cls.clock.tick(60)
            for func in funcs:
                func()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                for event_func in events:
                    event_func(event)

            cls.phyics_world.Step(
                cls.time_step,
                cls.ve_iters,
                cls.pos_iters
                )
            cls.scene.update()
            cls.scene.render(cls.screen)
            pygame.display.update()