import random
import pygame
from pygame_phyics.timertask import TimerTask

class Glitch:
    def __init__(self):
        self.timer = TimerTask(50)
        self.interval_timer = TimerTask(150)
    
    def _get_subsurface(self,surface, y):
        wid = surface.get_width()
        height = random.randrange(10, 20)
        shift = random.randint(10, 20)
        shift *= random.choice((1, -1))
        if y + height > surface.get_height():
            height = surface.get_height() - y

        sub = surface.subsurface((0, y, wid, height))
        sub_rect = sub.get_rect()
        result = pygame.Surface(sub_rect.size)

        result.blit(sub, (shift, 0))
        if shift > 0:
            sub_shift = sub.subsurface((0, 0, wid - shift, height))
            result.blit(sub_shift, (0, 0))
        else:
            sub_shift = sub.subsurface(abs(shift), 0, wid - abs(shift), height)
            result.blit(sub_shift, (wid - abs(shift), 0))
        return result

    def render(self, surface):
         if self.interval_timer.run_periodic_task():
            self.interval_timer.tick = int(random.uniform(0.2, 0.4) * 200)
            y_travelled = 0
            while y_travelled < surface.get_height():
                if random.random() > 0.8:
                    strip = self._get_subsurface(surface, y_travelled)
                    y_travelled += strip.get_height()
                    surface.blit(strip, (0, y_travelled))
                else:
                    y_travelled += random.randrange(10, 20)