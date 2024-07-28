import inspect

import pygame
import pygame_phyics.util as _util
from typing import List
from pygame_phyics.objects import *
from pygame_phyics.manger import Manger
from pygame_phyics.sheet import TileSheet, SurfaceSheet

class Scene:
    """여기로 오브젝트가 등록되고 공통함수를 실행합니다
    """
    
    def __init__(self):

        self.layers = [[],[],[],[],[],[],[],[]]

    def phyics_collison(self):
        for phyics in Physics.phyics_arr:
            phyics.collision()

    def phyics_set_location(self):
        for phyics in Physics.phyics_arr:
            phyics.set_location()

    def update(self):
        """등록된 객체에 update 함수를 실행합니다
        """
        for layer in self.layers:
            for obj in layer:
                obj.update()
                for component in obj.components:
                    component.update()
    
    def set_parent(self):
        for layer in self.layers:
            for obj in layer:
                obj.set_parent()
            
    
    def render(self, surface: pygame.Surface):
        """등록된 객체에 render 함수를 실행합니다

        Args:
            surface (pygame.Surface): 화면
        """
        for layer in self.layers:
            for obj in layer:
                if obj.visible:
                    obj.render(surface, self.camera)
                    for component in obj.components:
                        component.render(surface, self.camera)
    
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
        Manger.tile_sheet = {til[0] : TileSheet(*til) for til in setting.get('tile', [])}
        Manger.surface_sheet = {suf[0] : SurfaceSheet(*suf) for suf in setting.get('surface', [])}
        for key, value in setting.items():
            setattr(Manger, key, value)

        parent_object = ParentObject() # 우주 느낌
        parent_object.init_instantiate()

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
                        prefab.init_instantiate()
                    elif len(list(inspect.signature(prefab_class).parameters.keys())) == len(parameters):
                        raise ValueError(f"리스트에 길이는 같으나 이름이 틀리거나 순서가 다른것같습니다.\njson :{parameters}\n{name} class:{list(inspect.signature(prefab_class).parameters.keys())}")
                except ValueError as e:
                    print("Error message: ", e)
        
        self.set_parent()

        parent_object.location.set_world() # 각 오브젝트 world_position 생성
        
        self.phyics_set_location()

        self.display = setting.get('display', 'main_cam')