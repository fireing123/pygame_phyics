from pygame_phyics import util
from pygame_phyics.location import Location
from pygame_phyics.manger import Manger
from pygame_phyics.objects.object import Object
from pygame_phyics.vector import Vector


class GameObject(Object):
    """마우스 충돌 연산가능함"""
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag)
        self.visible = visible
        self.rect = None
        self.collide = 'out'
        self.location = Location(Vector(*position), rotation)
        self.parent_name = parent_name
    
    @util.getter
    def render_position(self):
        """y 좌표를 반전시켜줍니다
        pygame 은 화면에 그릴떄 y 선이 아래로 이동할수록 + 라서 
        사용자가 햇갈릴수 있기 떄문에 멥 파일에선 우리가 사용하는 방식으로작성하고
        그릴떄 좌표를 이것으로 사용하시면 됩니다.
        하지만 좌표가 topleft 기준입니다"""
        return Vector(self.location.world_position.x, Manger.HEIGHT - self.location.world_position.y)
    
    def set_parent(self):
        parent: GameObject = Manger.scene.get_objects(self.parent_name)[0]
        self.location.set_parent(parent.location)