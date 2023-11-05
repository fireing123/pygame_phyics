from pygame_phyics.vector import Vector
import pygame_phyics.util as _util
from pygame_phyics.manger import Manger

class Camera:
    """프로그렘이 바라보는 곳
    __call__ 로 호출헤서 반환 받은 튜플은 카메라 시선을 적용한 값이다
    x 랑 y 는 설정할수 없고 값을 얻을수만 있습니다 수정할려면 vector 값에서 접근하십시오
    """
    def __init__(self, x, y, angle):
        self.vector = Vector(x, y)
        self.__angle = angle
    # rect pass rotate 
    @property
    def angle(self):
        return self.__angle
    
    @angle.setter
    def angle(self, value):
        self.__angle = value if value < 360 else 360 - value

    @_util.getter
    def x(self):
        return self.vector.x
    
    @_util.getter
    def y(self):
        return self.vector.y
    
    def __call__(self, position: tuple[int, int] | Vector):
        """카메라 시선을 적용한 위치를 반환함

        Args:
            position (tuple[float, float] | Vector): 오브젝트에 위치

        Returns:
            tuple[float, float]: 카메라 시선이 적용된 위치
        """
        rotated = Vector(Manger.WIDTH/2, Manger.HEIGHT/2).rotate_vector(Vector(*position), self.angle)
        camerad = rotated - self.vector
        return camerad.xy
    
    def __getitem__(self, index):
        match index:
            case 0:
                return self.x
            case 1:
                return self.y

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index < 2:
            item = self[self.index]
            self.index += 1
            return item
        else:
            self.index = 0
            raise StopIteration
