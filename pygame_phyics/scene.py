import pygame_phyics.util as _util
from typing import List
from pygame_phyics.object import *
from pygame_phyics.manger import Manger
import inspect
class Camera:
    def __init__(self):
        self.__x = 0
        self.__y = 0
        self._index = 0
        self._len = 2
    
    def __call__(self, position):
        x = position[0] - self.x
        y = position[1] - self.y
        return x, y
    
    def __getitem__(self, index):
        return (self.x, self.y)[index]

    def __iter__(self):
        return iter((self.x, self.y))
    
    def __next__(self):
        next((self.x, self.y))
    
    @property
    def x(self):
        return self.__x
    
    @x.getter
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value
    
    @property
    def y(self):
        return self.__y
    
    @y.getter
    def y(self):
        return self.__y
    
    @y.setter
    def y(self, value):
        self.__y = value

class Scene:
    """새계임 여기로 오브젝트가 등록되고 공통함수를 실행함"""
    
    def __init__(self):
        self.camera = Camera()
        self.layers = [[],[],[],[],[],[],[],[]]
    
    def layer_loop(self, method, *args, **kwargs):
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
        self.layer_loop("update")
    
    def on_collision_enter(self):
        self.layer_loop("on_collision_enter", collide=True)
        self.layer_loop("clean_collision", only="phyics")
    
    def render(self, surface):
        self.layer_loop("render", surface, self.camera)
    
    def add(self, obj):
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
    
    def remove(self, obj):
        """오브젝트를 새계에서 삭제하지만 오브젝트 자체는 삭제되지않음"""
        
        try:
            self.layers[obj.layer].remove(obj)
        except ValueError:
            print('value error')
            
    def clear(self):
        """모든 오브젝트를 새계에서 삭제하고 오브젝트 객체도 삭제됨 (delete 함수 실행)"""
        
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
        """
        오브젝트를 생성하고 새계에 등록합니다

        Args:
            path (str): 경로
            class_list (list): 임포트한 클래스 리스트

        Raises:
            ImportError: path 경로에 json 에서 class_list 에 존재하지 않는 클래스를 불러오려 할때
        """
        json : dict = _util.jsopen(path)
        setting : dict = json['setting']
        
        if setting.get('camera'):
            self.camera.x = setting['camera'][0]
            self.camera.y = setting['camera'][1]
        setting.pop('camera')
        for key, value in setting.items():
            setattr(Manger, key, value)
        
        objs = json['objs']
        for name in objs.keys():
            for json_object in objs[name]:
                args = list(json_object.values())
                prefab_class = Manger.classes.get(name)
                if prefab_class == None:
                    prefab_class = globals()[name]
                    if prefab_class == None:
                        raise ImportError(f"{name} 클레스가 존재하지 않거나 불러지지 않았습니다. \n 현재 불러온 클래스 {Manger.classes}")
                prefab = prefab_class(*args)
                GameObject.instantiate(prefab)