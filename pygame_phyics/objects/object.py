from pygame_phyics.manger import Manger
from pygame_phyics.objects.component import Component


class Object(Component):
    """
    새상에 등록할수있는 가장 기초적인 오브젝트
    save 사용시 주의사항: 매개변수 이름이랑 저장용 변수 이름이랑 이름이 같아야합니다
    """
    
    def __init__(self, name, layer, tag):
        self.name = Manger.check_object_name(name)
        self.tag = tag
        self.layer = layer

    def delete(self): 
        """씬에서 이 오브젝트를 삭제합니다"""
        Manger.scene.remove(self)
        del self

    def instantiate(self):
        Manger.scene.add(self)