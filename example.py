import pygame
from pygame_phyics import game
from pygame_phyics import Game
from pygame_phyics.vector import Vector
from pygame_phyics import Manger
from pygame_phyics import DynamicObject
from pygame_phyics.object import InputField

Game.init((1000, 800), "MyGame")

Game.import_classes("example/objects/")

@game.world("example/example.json")
def example():
    text = Manger.scene.get_objects("eello")[0]
    inputfield : InputField = Manger.scene.get_objects("eeldlo")[0]
    def start(cls):
        text.text = 'hello\nworld!\n 한국어'

    def event(cls, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                cls.stop()
            if event.key == pygame.K_w:
                Manger.scene.camera.angle = 100
            if event.key == pygame.K_UP:
                Manger.scene.camera.vector.y += 10
            if event.key == pygame.K_DOWN:
                Manger.scene.camera.vector.y -= 10
            if event.key == pygame.K_LEFT:
                Manger.scene.camera.vector.x -= 10
            if event.key == pygame.K_RIGHT:
                Manger.scene.camera.vector.x += 10
    def update(cls):
        Manger.screen.fill((60, 60, 60, 255))
    return start, event, update



example()