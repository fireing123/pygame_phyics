"""object을 가져오고 object 를 새계에 생성하는 모듈"""

import os
import json
import importlib.util
import inspect
from typing import Dict

current_dir = os.path.dirname(os.path.abspath(__file__))

def import_module(import_dir):
    """
    폴더를 선회하며 가져온 클래스를 반환함
    
    Args:
        import_dir (str): 디랙토리 경로
        
    Returns:
        list: 클래스들
    
    """
    class_list = {}
    for file in os.listdir(import_dir):
        if file.endswith(".py") and file != '__init__.py':
            classes = import_classes(file[:-3], import_dir)
            class_list.update(classes)
    return class_list

def import_classes(file, dir):
    """
    모듈에서 가져온 클래스를 리스트로 반환함
    
    Args:
        file (str): 파일 이름
        dir (str): 폴더 경로
    
    Returns:
        list: 클래스들    
    """
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
    """
    오브젝트를 생성하고 새계에 등록합니다
    
    Args:
        path (str): 경로
        class_list (list): 임포트한 클래스 리스트
        
    Raises:
        ImportError: path 경로에 json 에서 class_list 에 존재하지 않는 클래스를 불러오려 할때
    """
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