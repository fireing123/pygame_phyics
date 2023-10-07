"""

게임 모듈 

Example:
    게임의 초기 샛팅을 실행하고 
    게임 맵을 정의하고
    실행한다
    literal blocks::

        $ Game.init((1000, 800), "MyGame")
        $
        $ @pygame_phyics.world("example/example.json")
        $ def main():
        $   Game.loop([], [])
        $   
        $ main()

"""

import pygame
from pygame import display

from Box2D import b2World
from pygame_phyics.manger import Manger
from pygame_phyics.scene import Scene
from pygame_phyics.mouse import mouse_event
from pygame_phyics.instantiate import import_module
from pygame_phyics.instantiate import load as instantiate_load
from pygame_phyics.input import Input
from pygame_phyics.event import Event
import pygame_phyics.mouse as mouse

def world(world_path: str):
    """
    함수를 새상으로 등록하는 데코레이터 입니다
    
    Args:
        world_path (str) : json 경로
    """
    def real_world(func):
        def wrapper():
            Manger.scene.darkening()
            Manger.world = b2World()
            Manger.scene = Scene()
            instantiate_load(world_path, Manger.classes)
            start, event, update = func()
            start()
            Manger.scene.brightening()
            Game.loop(event, update)
            del Manger.scene
        return wrapper
    return real_world

event_event = Event()

class Game:
    """게임 엔진"""
    is_running = True
    clock = pygame.time.Clock()
    time_step = 1 / 60
    ve_iters = 10
    pos_iters = 10
    
    @classmethod
    def init(cls, size : tuple[int, int], title : str):
        """개임 초기 샛팅입니다"""
        pygame.init()
        display.set_caption(title)
        Manger.init(
            display.set_mode(size),
            b2World(),
            Scene())
    
    @classmethod
    def import_classes(cls, obj_dir : str):
        """클래스들을 불러와 Manger 에 저장합니다"""
        Manger.classes.update(import_module(obj_dir))
        
    @classmethod
    def loop(cls, events, func):
        """이벤트랑 함수를 받아 반복문 안에서 실행합니다"""
        
        pygame.key.start_text_input()
        
        while cls.is_running:
            
            cls.clock.tick(60)
            
                    
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
                    
                event_event.invoke(event)
                
                events(event)

            Manger.world.Step(
                cls.time_step,
                cls.ve_iters,
                cls.pos_iters
                )
            
            Manger.scene.render(Manger.screen)
            pygame.display.update()