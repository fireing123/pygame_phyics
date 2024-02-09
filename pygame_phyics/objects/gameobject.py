from pygame_phyics import util
from pygame_phyics.manger import Manger
from pygame_phyics.objects.object import Object
from pygame_phyics.vector import Vector


class GameObject(Object):
    """마우스 충돌 연산가능함"""
    
    def __init__(self, name: str, tag, visible, layer):
        super().__init__(name, layer, tag)
        self.visible = visible
        self.rect = None
        self.collide = 'out'
    
    @util.getter
    def render_position(self):
        """y 좌표를 반전시켜줍니다
        pygame 은 화면에 그릴떄 y 선이 아래로 이동할수록 + 라서 
        사용자가 햇갈릴수 있기 떄문에 멥 파일에선 우리가 사용하는 방식으로작성하고
        그릴떄 좌표를 이것으로 사용하시면 됩니다.
        하지만 좌표가 topleft 기준입니다"""
        return Vector(self.position.x, Manger.HEIGHT - self.position.y)