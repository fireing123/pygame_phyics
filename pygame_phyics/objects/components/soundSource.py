import pygame
from pygame_phyics.objects.component import Component
from pygame_phyics.objects.components.soundListener import SoundListener

class SoundSource(Component):
    def __init__(self, object, path : str, volume, vol_lambda, mode=None):
        self.vol_lambda = vol_lambda
        self.object = object
        self.volume = volume
        match mode:
            case None:
                self.mode = "sound"
                self.sound = pygame.mixer.Sound(path)
            case "endPlay":
                self.mode = "end"
                self.sound = path

    def play(self, loops=0, maxtime=0, fade_ms=0, start=0):
        if self.mode == "sound":
            self.sound.play(loops, maxtime, fade_ms)
        elif self.mode == "end":
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.sound)
            pygame.mixer.music.play(loops, start, fade_ms)
        
    def stop(self):
        if self.mode == "sound":
            self.sound.stop()
        elif self.mode == "end":
            pygame.mixer.stop()
    
    def update(self):
        distance = self.object.location.world_position.distance_to(SoundListener.listener.object.location.world_position if SoundListener.listener != None else (0, 0))
        volume = self.vol_lambda(distance)
        self.sound.set_volume(volume + self.volume)
