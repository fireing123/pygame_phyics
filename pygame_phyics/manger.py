import pygame
import Box2D
# 내 모듈 임포트 못하는 모듈
class Manger:
    """정적 변수를 이곳에 저장함"""
    
    classes = {}
    
    @classmethod
    def init(cls, screen: pygame.Surface, world : Box2D.b2World , scene):
        """
        스크린, 물리, 일반을 저장함
        """
        cls.screen = screen
        cls.world = world
        cls.scene = scene