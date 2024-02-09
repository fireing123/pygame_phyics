import pygame
from pygame_phyics.camera import Camera

class Component:
    """기본 함수만 선언해놓음"""
    def on_mouse_enter(self, pos: tuple[int, int]):
        """마우스가 오브젝트(rect) 안에 들어올떄 호출됨

        Args:
            pos (tuple[int, int]): 마우스 위치 (접촉한 위치)
        """
        pass
    def on_mouse_stay(self, pos: tuple[int, int]):
        """마우스가 오브젝트(rect) 에서 들어온 상태일떄 계속 호출됨

        Args:
            pos (tuple[int, int]): 마우스 위치 (접촉한 위치)
        """
        pass
    def on_mouse_exit(self, pos: tuple[int, int]):
        """마우스가 오브젝트(rect) 에서 들어온 상태였다가 나오면 호출됨

        Args:
            pos (tuple[int, int]): 마우스 위치 (접촉한 위치)
        """
        pass
    def update(self):
        """게임 루프시 한번씩 실행됩니다"""
        pass
    def render(self, surface: pygame.Surface, camera: Camera):
        """씬에서 그릴때 실행합니다

        Args:
            surface (pygame.Surface): 프로그램 화면
            camera (Camera): 씬 카메라
        """
        pass
    