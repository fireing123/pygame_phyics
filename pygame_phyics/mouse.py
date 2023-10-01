from pygame_phyics.manger import Manger
from pygame.mouse import *

def mouse_event():
    try:
        for layer in Manger.scene.layers[::-1]:
            for obj in layer:
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