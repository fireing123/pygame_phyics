

class ImmutableAttributeError(Exception):
    """불변의 값을 수정할시 raise 한다"""
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
class JsonSerializableError(Exception):
    """값이 json 으로 파싱할수 없는 값일떄 raise 한다"""
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
class FunctionError(Exception):
    """함수가 아닐떄 raise 한다"""
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
class GameOver(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)