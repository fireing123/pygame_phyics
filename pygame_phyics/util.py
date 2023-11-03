from collections.abc import Callable
import math
import json as jsmodule
from pygame_phyics.error import JsonSerializableError
from pygame_phyics.error import ImmutableAttributeError

class const(property):
    """변수를 불변으로 만들고 싶을떄 프로퍼티처럼 사용하면 됩니다
    """
    def settar(self, value):
        raise ImmutableAttributeError("이 속성은 불변입니다 값을 할당하려 하지 마십시오")

class getter(property):
    """변수를 수정하기 싫을떄 프로퍼티처럼 사용하면 됩니다
    const 클래스와 다른점은 없지만 내부적으로 변수가 변할시 불변이랑 거리가 멀어서 새로 만들었습니다
    """
    def settar(self, value):
        raise ImmutableAttributeError("이 속성은 할당할수없습니다 값을 할당하려 하지 마십시오")

def string_insert(string: str, insert_string: str, index: int):
    """문자열에 문자열을 삽입합니다

    Args:
        string (str): 문자열
        insert_string (str): 삽입할 문자열
        index (int): 위치

    Raises:
        ValueError: 위치가 잘못된 값일떄

    Returns:
        str: 삽입된 문자열 
    """
    if len(string) < index or index < 0:
        raise ValueError(f"index 가 문자열에 유효한 위치가 아닙니다 string len: {len(string)} index: {index}")
    return f"{string[:index]}{insert_string}{string[index:]}"

def string_cut(string: str, range: tuple[int, int]):
    """일정 범위에 문자열을 잘라냅니다

    Args:
        string (str): 잘릴 문자열
        range (tuple[int, int]): 범위

    Raises:
        ValueError: 범위가 오름차순이 아닐떄

    Returns:
        _type_: _description_
    """
    if range[0] > range[1]:
        raise ValueError("범위에 끝은 처음보다 크거나 같아야합니다")
    return f"{string[:range[0]]}{string[range[1]:]}"

def jsopen(path: str) -> dict:
    """json 파일을 열어 dict 로 파싱합니다

    Args:
        path (str): json 경로

    Returns:
        dict: 파싱된 dict
    """
    with open(path, 'r') as f:
        json = jsmodule.loads(f.read())
    return json

def jsave(data: dict, path: str):
    """

    Args:
        data (dict): 저장할 딕셔너리
        path (str): 내보낼 경로
    """
    with open(path, 'w') as f:
        jsmodule.dump(data, f, indent=4)
        
types = (str, int, float, list, bool)

def check_json_serializable(dic: dict):
    """이 딕셔너리에서 json 으로 변환할수 없는 값이 있는지 검사합니다

    Args:
        dic (dict): 검사할 딕셔너리

    Raises:
        JsonSerializableError: json 에서 저장할수 없는 타입이 발견될시
    """
    for value in list(dic.values()):
        if isinstance(value, types):
            pass
        elif isinstance(value, dict):
            check_json_serializable(value)
        else:
            raise JsonSerializableError(f"{type(value)} 타입은 json 에 저장할수 있는 타입이 아닙니다")

