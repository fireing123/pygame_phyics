
class ImmutableAttributeError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
    
class JsonSerializableError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
class FunctionError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
class GameOver(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)