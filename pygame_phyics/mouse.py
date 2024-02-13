"""
pygame 의 마우스르 상속받음
"""
from pygame_phyics.manger import Manger
from pygame.mouse import *

def mouse_event():
    """rect 를 가진 오브젝트의 마우스 충돌을 연산함

    Raises:
        NotImplementedError: 마우스 충돌은 가장 위 레이어 에만 호출 되어야만 한다
        NotImplementedError: 마우스 충돌은 가장 위 레이어 에만 호출 되어야만 한다
        NotImplementedError: 마우스 충돌은 가장 위 레이어 에만 호출 되어야만 한다
    """
    
    try:
        for layer in Manger.scene.layers[::-1]:
            for obj in layer[::-1]:
                if obj.rect != None:
                    if obj.rect.collidepoint(get_pos()):
                        if obj.collide == 'out':
                            obj.collide = 'in'
                            obj.on_mouse_enter(get_pos())
                            raise NotImplementedError
                        elif obj.collide == 'in':
                            obj.on_mouse_stay(get_pos())
                            raise NotImplementedError
                    elif obj.collide == 'in':
                        obj.collide = 'out'
                        obj.on_mouse_exit(get_pos())
                        raise NotImplementedError
    except:
        pass