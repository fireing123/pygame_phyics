from pygame_phyics.objects.gameobject import GameObject
from pygame_phyics.vector import Vector


class UI(GameObject):
    """ui 를 위한 오브젝트"""
    def __init__(self, name: str, tag, visible, layer, position, angle):
        super().__init__(name, tag, visible, layer)
        self.position : Vector = Vector(*position)
        self.angle = angle