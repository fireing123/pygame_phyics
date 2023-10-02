import pygame
from pygame import display

from Box2D import b2World
from pygame_phyics.manger import Manger
from pygame_phyics.scene import Scene
from pygame_phyics.event import Event
from pygame_phyics.mouse import mouse_event
from pygame_phyics.instantiate import import_module, import_classes
from pygame_phyics.instantiate import load as instantiate_load
from pygame_phyics.input import Input
import pygame_phyics.mouse as mouse

def world(world_path):
    def real_world(func):
        def wrapper():
            Manger.scene.darkening()
            Manger.world = b2World()
            Manger.scene = Scene()
            instantiate_load(world_path, Manger.classes)
            Manger.scene.brightening()
            func()
            del Manger.scene
        return wrapper
    return real_world

events = {
    ""
}

def event(event_type):
    def real_event(func):
        return func
    events[event_type] = real_event
    return real_event

class Game:
    
    is_running = True
    clock = pygame.time.Clock()
    time_step = 1 / 60
    ve_iters = 10
    pos_iters = 10
    
    @classmethod
    def init(cls, size, title):
        pygame.init()
        display.set_caption(title)
        Manger.init(
            display.set_mode(size),
            b2World(),
            Scene())
        Manger.classes.update(import_classes('object', 'pygame_phyics/'))
    
    @classmethod
    def import_classes(cls, obj_dir):
        Manger.classes.update(import_module(obj_dir))
        
    @classmethod
    def loop(cls, events=[], funcs=[]):
        
        pygame.key.start_text_input()
        
        while cls.is_running:
            
            cls.clock.tick(60)
            
                    
            for func in funcs:
                func()
            
            #collider event
            
            mouse_pressed = mouse.get_pressed()
            
            for i in range(3):
                mouse_click = Input.mouse_click[i]
                if mouse_pressed[i]:
                    if mouse_click <= 1:
                        Input.mouse_click[i] = 2
                    else:
                        Input.mouse_click[i] = 3
                else:
                    if mouse_click >= 2:
                        Input.mouse_click[i] = 1
                    else:
                        Input.mouse_click[i] = 0
                        
            mouse_event()
            
            Manger.scene.update()
            
            for key, value in Input.key_board.items():
                if value == 2:
                    Input.key_board[key] = 3
                elif value == 1:
                    Input.key_board[key] = 0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.KEYDOWN:
                    Input.key_board[event.key] = 2
                elif event.type == pygame.KEYUP:
                    Input.key_board[event.key] = 1
                for event_func in events:
                    event_func(event)

            Manger.world.Step(
                cls.time_step,
                cls.ve_iters,
                cls.pos_iters
                )
            
            Manger.scene.render(Manger.screen)
            pygame.display.update()