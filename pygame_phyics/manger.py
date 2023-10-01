# 내 모듈 임포트 못하는 모듈
class Manger:
    
    classes = {}
    
    @classmethod
    def init(cls, screen, world, scene):
        cls.screen = screen
        cls.world = world
        cls.scene = scene