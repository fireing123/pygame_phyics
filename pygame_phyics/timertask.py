import inspect
from pygame import time
from typing import Callable
from pygame_phyics.error import FunctionError

class TimerTask:
    """틱마다 이벤트를 실행합니다
    **주의사항 int 나 str 같은것들은 생성 당시 값을 가지므로
    실시간 숫자를 가져오려면 람다식을 사용하시는게 좋습니다
    """
    def __init__(self, tick: int, event: Callable, *value, **kwargs):
        """틱마다 이벤트를 실행합니다
        **주의사항 int 나 str 같은것들은 생성 당시 값을 가지므로
        실시간 숫자를 가져오려면 람다식을 사용하시는게 좋습니다
        
        Args:
            tick (int): 실행 간격
            event (Callable): 실행할 함수

        Raises:
            FunctionError: 주어진 event 가 함수가 아닐떄
        """
        self.tick = tick
        self.last_update = 0
        if inspect.ismethod(event) and inspect.isfunction(event):
            raise FunctionError(f"입력받은 값은 는 함수가 아닙니다")
        self.event = event
        self.value = value
        self.kwargs = kwargs
        
    def run_periodic_task(self):
        """주기적으로 실행해주기 위해선 이함수를 실행해야한다
        원리가 조건이 맞으면 실행되는거라 이 함수에 실행 개수가 아닙니다
        이 함수는 반복실행되는 곳에서 사용하는게 적합합니다
        update, event, render 같은 곳이 예시입니다

        Returns:
            _type_: _description_
        """
        if time.get_ticks() - self.last_update > self.tick:
            self.last_update = time.get_ticks()
            self.event(*self.value, **self.kwargs)
            return True
        return False
    
    def reset(self):
        """기다리는것을 처음으로 되돌린다 생각하면 됩니다
        재생중인 영상을 처음으로 이동하는것처럼
        """
        self.last_update = time.get_ticks()
        
class OnceTimerTask(TimerTask):
    """한번 실행되는 TimerTask 
    리셋되멘 다시 실행할수 있다
    기다릴떄 리셋하고 실행하는게 좋을것같다
    """
    def __init__(self, tick, event, *value, **kwargs):
        super().__init__(tick, event, *value, **kwargs)
        self.once = False
    
    def run_periodic_task(self):
        if time.get_ticks() - self.last_update > self.tick and not self.once:
            self.event(*self.value, **self.kwargs)
            self.once = True
            return True
        return False
    
    def reset(self):
        super().reset()
        self.once = False
    