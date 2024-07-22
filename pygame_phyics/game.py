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

from Box2D import b2World, b2ContactListener
from typing import Callable
from pygame_phyics.manger import Manger
from pygame_phyics.scene import Scene
from pygame_phyics.mouse import mouse_event
from pygame_phyics.instantiate import import_module
from pygame_phyics.input import Input
from pygame_phyics.event import Event
from pygame_phyics.objects import Physics
import pygame_phyics.mouse as mouse


class ContactListener(b2ContactListener):
    """물리 새상에서 충돌 연산을 GameObject 로 꺼낼수 있게 도와줌"""
    def BeginContact(self, contact):
        fixtureA = contact.fixtureA
        fixtureB = contact.fixtureB
        a_obj : Physics = fixtureA.body.userData 
        b_obj : Physics = fixtureB.body.userData
        if a_obj != None:
            a_obj.collide_enter.append(b_obj)
        else:
            raise ValueError("충돌한 물리 객체의 GameObject가 존재하지 않음." , a_obj)
        if b_obj != None:
            b_obj.collide_enter.append(a_obj)
        else:
            raise ValueError("충돌한 물리 객체의 GameObject가 존재하지 않음." , b_obj)

def world(world_path: str):
    """함수를 새상으로 등록하는 데코레이터 입니다
    
    Args:
        world_path (str) : json 경로
    """
    def real_world(func):
        def wrapper():
            Manger.world = b2World()
            contact_listener = ContactListener()
            Manger.world.contactListener = contact_listener
            Manger.scene = Scene()
            Manger.scene.load(world_path)
            start, event, update = func()
            start(Game)
            Game.loop(event, update)
            del Manger.scene
            del Manger.world
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
        """게임에 초기 설정을 진행합니다

        Args:
            size (tuple[int, int]): 스크린 크기입니다
            title (str): 프로그램에 제목입니다
        """
        pygame.init()
        display.set_caption(title)
        pygame.key.start_text_input()
        Manger.init(display.set_mode(size), Scene())
    
    @classmethod
    def import_objects(cls, obj_dir : str, **kwargs):
        """클래스들을 불러와 Manger 에 저장합니다

        Args:
            obj_dir (str): 오브젝트 클래스에 파일를 저장한 폴더 경로
        """
        Manger.classes.update(import_module(obj_dir, **kwargs))
    
    @classmethod
    def stop(cls):
        cls.is_running = False
    
    @classmethod
    def loop(cls, events: Callable, func: Callable):
        """이벤트랑 함수를 받아 반복문 안에서 실행합니다

        Args:
            events (Callable): 이벤트 떄 실행됨
            func (Callable): 루프 돌때 실행됨
        """
        
        while cls.is_running:
            cls.clock.tick(60)
            
            func(cls)
            
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
                
                events(cls, event)

            Manger.scene.update()
            
            Manger.scene.on_collision_enter()

            Manger.world.Step(
                cls.time_step,
                cls.ve_iters,
                cls.pos_iters
                )
            
            Manger.scene.render(Manger.screen)

            if Manger.scene.camera.status == 'glitch':
                Manger.scene.camera.glitch.render(Manger.screen)

            pygame.display.update()