import os
import json
import importlib.util
import inspect
from typing import Dict

current_dir = os.path.dirname(os.path.abspath(__file__))

def import_module(import_dir):
    class_list = {}
    for file in os.listdir(import_dir):
        if file.endswith(".py") and file != '__init__.py':
            classes = import_classes(file[:-3], import_dir)
            class_list.update(classes)
    return class_list

def import_classes(file, dir):
    class_list = {}
    spec = importlib.util.spec_from_file_location(file, dir + file + ".py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    try:
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and hasattr(obj, 'instantiate'):
                print(f"Imported class: {name} from {file}")
                class_list[name] = obj
    except ImportError as e:
        print(f"모듈 {file}을(를) 임포트하는 중 오류 발생: {e}")
    finally:
        return class_list

def load(path: str, class_list):
    GameObject = class_list['GameObject']
    with open(path, 'r') as f:
        js : Dict = json.loads(f.read())
        for name in js.keys():
            for json_object in js[name]:
                args = list(json_object.values())
                prefab_class = class_list.get(name)
                if prefab_class == None:
                    raise ImportError(f"{name} 클레스가 존재하지 않거나 불러지지 않았습니다. \n 현재 불러온 클래스 {class_list}")
                prefab = prefab_class(*args)
                GameObject.instantiate(prefab)