import pygame
from pygame_phyics import game
from pygame_phyics import Game
from pygame_phyics import Manger
from pygame_phyics import DynamicObject
from pygame_phyics.object import InputField

Game.init((1000, 800), "MyGame")

Game.import_classes("example/objects/")

@game.phyics_world("example/example.json")
def example():
    rect : DynamicObject= Manger.scene.get_objects("hello")[0]
    circle = Manger.scene.get_objects("ello")[0]
    text = Manger.scene.get_objects("eello")[0]
    inputfield : InputField = Manger.scene.get_objects("eeldlo")[0]
    def start(cls):
        text.text = 'hello\nworld!\n 한국어'
        rect.create_joint(4.0, 0.5, circle)
        def inputd(text):
            print(text)
        inputfield.input_event.add_lisner(inputd)
    def event(cls, event):
        if event.type == pygame.K_q:
            cls.stop()
    def update(cls):
        Manger.screen.fill((60, 60, 60, 255))
    return start, event, update



example()