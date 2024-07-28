import pygame
from pygame_phyics import game
from pygame_phyics import Game
from pygame_phyics import Manger
from pygame_phyics import GameObject
from pygame_phyics import Vector
from pygame_phyics.objects import InputField

Game.init((1000, 800), "MyGame")

#Game.import_objects("objects/")

@game.world("example.json")
def example():
    text : GameObject = Manger.scene.get_objects("eello")[0]
    #inputfield : InputField = Manger.scene.get_objects("eeldlo")[0]
    def start(cls):
        cls.camera = Manger.scene.camera.location
        text.text = 'hello\nworld!\n 한국어'
        text.location.position = Vector(0, 200)
    def event(cls, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                cls.stop()
            if event.key == pygame.K_w:
                cls.camera.rotation += 20
            if event.key == pygame.K_UP:
                c = cls.camera.position
                c.y += 10
                cls.camera.position = c
            if event.key == pygame.K_DOWN:
                c = cls.camera.position
                c.y -= 10
                cls.camera.position = c
            if event.key == pygame.K_LEFT:
                c = cls.camera.position
                c.x -= 10
                cls.camera.position = c
            if event.key == pygame.K_RIGHT:
                c = cls.camera.position
                c.x += 10
                cls.camera.position = c
            
    def update(cls):
        Manger.screen.fill((60, 60, 60, 255))
    return start, event, update



example()