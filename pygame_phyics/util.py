import json as jsmodule
from pygame_phyics.error import JsonSerializableError

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