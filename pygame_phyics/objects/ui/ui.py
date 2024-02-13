from pygame_phyics.objects.gameobject import GameObject
from pygame_phyics.vector import Vector


class UI(GameObject):
    """ui 를 위한 오브젝트"""
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)