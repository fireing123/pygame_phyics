from collections.abc import Callable
import math
import json as jsmodule
from pygame_phyics.error import JsonSerializableError
from pygame_phyics.error import ImmutableAttributeError

class const(property):
    def settar(self, value):
        raise ImmutableAttributeError("이 속성은 불변입니다 값을 할당하려 하지 마십시오")

class getter(property):
    def settar(self, value):
        raise ImmutableAttributeError("이 속성은 할당할수없습니다 값을 할당하려 하지 마십시오")

def string_insert(string: str, insert_string: str, index: int):
    if len(string) < index:
        raise ValueError(f"index 가 문자열에 최대 길이보다 깁니다 string len: {len(string)} index: {index}")
    return f"{string[:index]}{insert_string}{string[index:]}"

def string_cut(string: str, range: tuple[int, int]):
    if range[0] > range[1]:
        raise ValueError("범위에 끝은 처음보다 크거나 같아야합니다")
    return f"{string[:range[0]]}{string[range[1]:]}"

def jsopen(path):
    with open(path, 'r') as f:
        json = jsmodule.loads(f.read())
    return json

def jsave(data, path):
    
    with open(path, 'w') as f:
        jsmodule.dump(data, f, indent=4)
        
types = (str, int, float, list, bool)

def check_json_serializable(dic: dict):
    for value in list(dic.values()):
        if isinstance(value, types):
            pass
        elif isinstance(value, dict):
            check_json_serializable(value)
        else:
            raise JsonSerializableError(f"{type(value)} 타입은 json 에 저장할수 있는 타입이 아닙니다")

