import pygame
from pygame_phyics import game
from pygame_phyics import Game
from pygame_phyics import Manger
from pygame_phyics import GameObject
from pygame_phyics.objects import InputField

Game.init((1000, 800), "MyGame")

#Game.import_objects("objects/")

@game.world("example.json")
def example():
    text : GameObject = Manger.scene.get_objects("eello")[0]
    inputfield : InputField = Manger.scene.get_objects("eeldlo")[0]
    def start(cls):
        text.text = 'hello\nworld!\n 한국어'
        print(text.location.position)
    def event(cls, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                cls.stop()
            if event.key == pygame.K_w:
                Manger.scene.camera.location.roation += 20
            if event.key == pygame.K_UP:
                Manger.scene.camera.location.position.y += 10
            if event.key == pygame.K_DOWN:
                Manger.scene.camera.location.position.y -= 10
            if event.key == pygame.K_LEFT:
                Manger.scene.camera.location.position.x -= 10
            if event.key == pygame.K_RIGHT:
                Manger.scene.camera.location.position.x += 10
            
    def update(cls):
        Manger.screen.fill((60, 60, 60, 255))
    return start, event, update



example()