import inspect
from pygame import time
from pygame_phyics.error import FunctionError

class TimerTask:
    def __init__(self, tick, event, *value, **kwargs):
        self.tick = tick
        self.last_update = 0
        if not inspect.ismethod(event):
            raise FunctionError(f"입력받은 값은 는 함수가 아닙니다")
        self.event = event
        self.value = value
        self.kwargs = kwargs
        
    def run_periodic_task(self):
        if time.get_ticks() - self.last_update > self.tick:
            self.last_update = time.get_ticks()
            self.event(*self.value, **self.kwargs)
            return True
        return False
    
    def reset(self):
        self.last_update = time.get_ticks()