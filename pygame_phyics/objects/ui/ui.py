from pygame_phyics.objects.gameobject import GameObject
from pygame_phyics.vector import Vector


class UI(GameObject):
    """ui 를 위한 오브젝트"""
    def __init__(self, supe):
        super().__init__(*supe)