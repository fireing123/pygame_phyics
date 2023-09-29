
class ImmutableAttributeError(Exception):
    def __init__(self, cls, attribute_name):
        self.message = f'{cls}의 {attribute_name} 속성은 불변입니다. 값을 변경할 수 없습니다.'
        super().__init__(self.message)
    
class GameOver(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)