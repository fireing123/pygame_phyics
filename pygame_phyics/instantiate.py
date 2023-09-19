import os
import json
import importlib.util
import inspect
from typing import Dict

current_dir = os.path.dirname(os.path.abspath(__file__))

def import_classes(import_dir):
    class_list = {}
    for file in os.listdir(import_dir):
        if file.endswith(".py") and file != '__init__.py':
            module_name = file[:-3]
            spec = importlib.util.spec_from_file_location(module_name, import_dir + module_name + ".py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            try:
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj):
                        print(f"Imported class: {name} from {module_name}")
                        class_list[name] = obj
            except ImportError as e:
                print(f"모듈 {module_name}을(를) 임포트하는 중 오류 발생: {e}")
    return class_list

def load(path: str, class_list):
    from pygame_phyics.object import GameObject
    with open(path, 'r') as f:
        js : Dict = json.loads(f.read())
        for name in js.keys():
            for json_object in js[name]:
                args = list(json_object.values())
                obj = class_list[name](*args)
                GameObject.instantiate(obj)