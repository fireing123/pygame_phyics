import os
import json
import importlib
import inspect
from typing import Dict

def import_classes(import_dir):
    class_list = {}
    for file in os.listdir(import_dir):
        if file.endswith(".py") and file != '__init__.py':
            module_name = file[:-3]
            try:
                module = importlib.import_module(module_name)
                
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj):
                        print(f"Imported class: {name} from {module_name}")
                        class_list[name] = obj
            except ImportError as e:
                print(f"모듈 {module_name}을(를) 임포트하는 중 오류 발생: {e}")
    return class_list

def load(path: str, class_list):
    with open(path, 'r') as f:
        js : Dict = json.loads(f.read())
        for name in js.keys():
            for json_object in js[name]:
                class_list[name].instantiate(json_object)