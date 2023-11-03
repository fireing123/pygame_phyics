"""GameObject 를 Scene 에 등록하는 모듈"""

import os
import importlib.util
import inspect

current_dir = os.path.dirname(os.path.abspath(__file__))
"""절대경로"""


def import_module(import_dir) -> list:
    """폴더를 선회하며 가져온 클래스를 반환함
    **주의사항 폴더 끝에 / 를 붙여야함
    
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

def import_classes(file: str, dir: str) -> list:
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
