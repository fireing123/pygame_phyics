from pygame import Surface
from pygame_phyics.camera import Camera
from pygame_phyics.objects.object import Object
from pygame_phyics.location import Location
from pygame_phyics.vector import Vector
from pygame_phyics.manger import Manger
from pygame_phyics.effect import Glitch

class CameraObject(Object):
    def __init__(self, name, tag, position, rotation):
        super().__init__(name, 0, tag)
        self.visible = False
        self.status = "idle"
        self.rect = None
        self.collide = 'out'
        self.glitch = Glitch()
        self.location = Location(Vector(*position), rotation)

    def set_parent(self):
        parent = Manger.scene.get_objects("parent")[0]
        self.location.set_parent(parent.location)

    def __call__(self, position: tuple[int, int] | Vector):
        """카메라 시선을 적용한 위치를 반환함

        Args:
            position (tuple[float, float] | Vector): 오브젝트에 위치

        Returns:
            tuple[float, float]: 카메라 시선이 적용된 위치
        """
        rotated = Vector(Manger.WIDTH/2, Manger.HEIGHT/2).rotate_vector(Vector(*position), self.location.rotation)
        camerad = rotated - self.location.position
        return camerad.xy

    def render(self, surface: Surface, camera: Camera):
        surface.fill((127, 127, 127))