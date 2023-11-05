import inspect
import pygame_phyics.util as _util
from pygame_phyics.vector import Vector
from typing import List, Callable
from pygame_phyics.object import *
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


class Scene:
    """여기로 오브젝트가 등록되고 공통함수를 실행합니다
    """
    
    def __init__(self):
        self.camera = Camera(0, 0, 0)
        self.layers = [[],[],[],[],[],[],[],[]]
    
    def layer_loop(self, method: str, *args, **kwargs):
        """레이어를 순환하며 겍체에 method 를 실행합니다

        Args:
            method (str): 실행할 함수 이름 
        """
        for layer in self.layers:
            for obj in layer:
                if kwargs.get("only") == "phyics":
                    if isinstance(obj, Phyics):
                        func = getattr(obj, method)
                        func(*args)
                elif kwargs.get('collide'):
                    if getattr(obj, "collide_enter", None) != None:
                        func = getattr(obj, method)
                        func(obj.collide_enter)
                else:
                    func = getattr(obj, method)
                    func(*args)
    
    def update(self):
        """등록된 객체에 update 함수를 실행합니다
        """
        self.layer_loop("update")
    
    def on_collision_enter(self):
        """충돌 함수를 호출합니다
        """
        self.layer_loop("on_collision_enter", collide=True)
        self.layer_loop("clean_collision", only="phyics")
    
    def render(self, surface: pygame.Surface):
        """등록된 객체에 render 함수를 실행합니다

        Args:
            surface (pygame.Surface): 화면
        """
        self.layer_loop("render", surface, self.camera)
    
    def add(self, obj: GameObject):
        """
        오브젝트를 추가함
        
        Args:
            obj (GameObject): GameObject 를 상속받것들
        
        """
        layer = self.layers[obj.layer]
        layer.append(obj)
    
    def absorb(self, list : List):
        """
        오브젝트 집합을 추가함
        
        Args:
            list (list): 오브젝트 리스트
        
        """
        for obj in list:
            self.add(obj)
    
    def remove(self, obj: GameObject):
        """오브젝트를 새계에서 삭제하지만 오브젝트 자체는 삭제되지않음"""
        
        try:
            self.layers[obj.layer].remove(obj)
        except ValueError:
            raise ValueError("이미 삭제 되었거나 다른 레이어 계층에 있는것 같습니다")
            
    def clear(self):
        """모든 오브젝트를 새계에서 삭제하고 오브젝트 객체도 삭제됨 (delete 함수 실행)
        """
        for layer in self.layers:
            for _ in range(len(layer)):
                layer[0].delete()
    
    def get_objects(self, obj_name):
        """
        입력받은 이름을 가진 오브젝트들을 반환함
        
        Args:
            obj_name (str): 오브젝트 이름
            
        Returns:
            list: 오브젝트들
        """
        objs = []
        for layer in self.layers:
            for i in range(len(layer)):
                if layer[i].name == obj_name:
                    objs.append(layer[i])
        return objs
    
    def __del__(self):
        self.clear()
        del self.layers
        del self.camera
    
    def darkening(self):
        """
        화면 전환시 실행돠는 함수
        따로 override 해서 사용하세요
        """
        pass
    
    def brightening(self):
        """
        화면 전환시 실행돠는 함수
        따로 override 해서 사용하세요
        """
        pass

    def load(self, path: str):
        """오브젝트를 생성하고 새계에 등록합니다

        Args:
            path (str): 멥 파일에 경로 .json

        Raises:
            ImportError: path 경로에 json 에서 class_list 에 존재하지 않는 클래스를 불러오려 할때
            ValueError: 매개변수와 json 에서 저장된 값에 이름이 다르면
        """
        json : dict = _util.jsopen(path)
        setting : dict = json['setting']
        
        if setting.get('camera') != None:
            self.camera.vector.x = setting['camera'][0]
            self.camera.vector.y = setting['camera'][1]
            self.camera.angle = setting['camera'][2]
            setting.pop('camera')
        for key, value in setting.items():
            setattr(Manger, key, value)
        
        objs = json['objs']
        for name in objs.keys():
            for json_object in objs[name]:
                args = list(json_object.values())
                parameters = list(json_object.keys())
                prefab_class = Manger.classes.get(name)
                if prefab_class == None:
                    prefab_class = globals()[name]
                    if prefab_class == None:
                        raise ImportError(f"{name} 클레스가 존재하지 않거나 불러지지 않았습니다. \n 현재 불러온 클래스 {Manger.classes}")
                if list(inspect.signature(prefab_class).parameters.keys()) == parameters:
                    prefab = prefab_class(*args)
                    GameObject.instantiate(prefab)
                elif len(list(inspect.signature(prefab_class).parameters.keys())) == len(parameters):
                    raise ValueError(f"리스트에 길이는 같으나 이름이 틀리거나 순서가 다른것같습니다.\njson :{parameters}\nclass:{list(inspect.signature(prefab_class).parameters.keys())}")