from typing import List, Callable

class Event:
    """
    이 클래스는 함수들을 받아 특정상황에 실행합니다
    
    Attributes:
        lisners: A list include functions
    """
    def __init__(self):
        self.lisners : List[Callable] = []
    
    def __call__(self):
        self.invoke()
    
    def __len__(self):
        return len(self.lisners)
    
    def add_lisner(self, function: Callable):
        """함수를 인자로 받아 함수를 등록합니다."""
        self.lisners.append(function)
    
    def invoke(self, *arg):
        """lisners의 함수들을 실행합니다."""
        for function in self.lisners:
            function(*arg)