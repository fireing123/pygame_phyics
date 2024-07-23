import inspect

import pygame
import pygame_phyics.util as _util
from typing import List
from pygame_phyics.objects import *
from pygame_phyics.manger import Manger
from pygame_phyics.sheet import TileSheet, SurfaceSheet
from pygame_phyics.collison import Collison
class Scene:
    """여기로 오브젝트가 등록되고 공통함수를 실행합니다
    """
    
    def __init__(self):

        self.layers = [[],[],[],[],[],[],[],[]]
    
    def layer_loop(self, method: str, *args, **kwargs):
        """레이어를 순환하며 겍체에 method 를 실행합니다

        Args:
            method (str): 실행할 함수 이름 
        """
        for layer in self.layers:
            for obj in layer:
                func = getattr(obj, method, None)
                if kwargs.get("only") == "phyics":
                    if isinstance(obj, Physics):
                        if kwargs.get('collide'):
                            if len(obj.collide_enter) != 0:
                                for collide in obj.collide_enter:
                                    collison = Collison(collide, obj)
                                    func(collison)
                        else:
                            func(*args)
                else:
                    func(*args)
    
    def update(self):
        """등록된 객체에 update 함수를 실행합니다
        """
        self.layer_loop("update")
    
    def set_parent(self):
        self.layer_loop("set_parent")
    
    def on_collision_enter(self):
        """충돌 함수를 호출합니다
        """
        self.layer_loop("on_collision_enter", only="phyics", collide=True)
        self.layer_loop("clean_collision", only="phyics")
    
    def set_physics_location(self): 
        self.layer_loop("set_location", only='phyics')
    
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
    
    @property
    def display(self):
        return self.__display
    
    @display.setter
    def display(self, value):
        self.__display = value
        self.camera = self.get_objects(value)[0]

    def __del__(self):
        self.clear()
        del self.layers
    
    def darkening(self):
        """적합하지 않다 판단됨 [사용되지 않음]"""
        pass
    
    def brightening(self):
        """적합하지 않다 판단됨 [사용되지 않음]"""
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
        Manger.tile_sheet = {til[0] : TileSheet(*til) for til in setting['tile']}
        Manger.surface_sheet = {suf[0] : SurfaceSheet(*suf) for suf in setting['surface']}
        for key, value in setting.items():
            setattr(Manger, key, value)
        
        objs = json['objs']
        for name in objs.keys():
            for json_object in objs[name]:
                try:
                    args = list(json_object.values())
                    parameters = list(json_object.keys())
                    prefab_class = Manger.classes.get(name)
                    if prefab_class == None:
                        prefab_class = globals()[name]
                        if prefab_class == None:
                            raise ImportError(f"{name} 클레스가 존재하지 않거나 불러지지 않았습니다. \n 현재 불러온 클래스 {Manger.classes}")
                    if list(inspect.signature(prefab_class).parameters.keys()) == parameters:
                        prefab = prefab_class(*args)
                        prefab.instantiate()
                    elif len(list(inspect.signature(prefab_class).parameters.keys())) == len(parameters):
                        raise ValueError(f"리스트에 길이는 같으나 이름이 틀리거나 순서가 다른것같습니다.\njson :{parameters}\n{name} class:{list(inspect.signature(prefab_class).parameters.keys())}")
                except ValueError as e:
                    print("Error message: ", e)
        

        self.set_parent()
        
        self.set_physics_location()

        self.display = setting.get('display', 'main_cam')