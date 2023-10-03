import pygame
import Box2D
# 내 모듈 임포트 못하는 모듈
class Manger:
    """정적 변수를 이곳에 저장함"""
    
    classes = {}
    
    @classmethod
    def init(cls, screen, world, scene):
        """
        스크린, 물리, 일반을 저장함
        """
        cls.screen : pygame.Surface = screen
        cls.world : Box2D.b2World = world
        cls.scene = scene