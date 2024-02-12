"""GameObject 를 Scene 에 등록하는 모듈"""

import os
import importlib.util
import inspect

current_dir = os.path.dirname(os.path.abspath(__file__))
"""절대경로"""


def import_module(import_dir, **kwargs):
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
            classes = import_classes(file[:-3], import_dir, **kwargs)
            class_list.update(classes)
        elif os.path.isdir(file):
            class_list += import_module(import_dir + file + "/", **kwargs)
        else:
            if kwargs.get('debug', "default") == 'detail':
                print(f"ignored file {file}")
    return class_list

def import_classes(file: str, dir: str, **kwargs) -> dict:
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
                if not name.startswith("_"):
                    if kwargs.get('debug', "default") == 'log':
                        print(f"Imported class: {name} from {file}.py")
                    elif kwargs.get('debug', "default") == 'detail':
                        print(f"Imported class: {name} from {file}.py\nDir: {dir + file}.py")
                    class_list[name] = obj
            else:
                if kwargs.get('debug', "default") == 'detail':
                    if not name.startswith("__"):
                        print(f"ignored: {name} from {file}.py")
    except ImportError as e:
        print(f"모듈 {file}을(를) 임포트하는 중 오류 발생: {e}")
    finally:
        return class_list
