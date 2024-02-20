import pygame
import re

# 내 모듈 임포트 못하는 모듈
class Manger:
    """정적 변수를 이곳에 저장함"""
    
    classes = {}
    obj_names = []

    @classmethod
    def check_object_name(cls, name: str):
        for obn in cls.obj_names:
            if obn == name:
                intr: str = re.compile('\(([^)]+)').findall(name)[-1]
                if intr and intr.isdigit():
                    return cls.check_object_name(name.replace(f"({intr})", f"({int(intr) + 1})"))
                return name + " (1)"
            else:
                continue
        return name

    @classmethod
    def init(cls, screen: pygame.Surface, none_scene):
        """게임에 정적 변수 초기 설정 함수

        Args:
            screen (pygame.Surface): 프로그램 스크린
            none_scene (Scene): 공백인 씬
        """
        cls.screen = screen
        cls.scene = none_scene
        cls.WIDTH, cls.HEIGHT = screen.get_size()