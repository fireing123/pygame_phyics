import pygame_phyics
from pygame_phyics.game import Game
from pygame_phyics import Manger
from pygame_phyics import DynamicObject

Game.init((1000, 800), "MyGame")

Game.import_classes("example/objects/")

@pygame_phyics.world("example/example.json")
def main():
    rect : DynamicObject= Manger.scene.get_objects("hello")[0]
    circle = Manger.scene.get_objects("ello")[0]
    text = Manger.scene.get_objects("eello")[0]
    inputfield = Manger.scene.get_objects("eeldlo")[0]
    text.text = 'hello\nworld!\n 한국어'
    rect.create_joint(4.0, 0.5, circle)
    def draw():
        Manger.screen.fill((60, 60, 60, 255))
    
    Game.loop([inputfield.inputfield_event], [draw])


main()