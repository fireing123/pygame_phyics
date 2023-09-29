from pygame_phyics.game import Game
from pygame_phyics import DynamicObject
from pygame_phyics.game import world
from pygame_phyics.mouse import mouse_event

Game.init((1000, 800), "MyGame")

Game.import_objects("example/objects/")

@world("example/example.json")
def main():
    rect : DynamicObject= Game.scene.get_objects("hello")[0]
    circle = Game.scene.get_objects("llo")[0]
    rect.CreateJoint(4.0, 0.5, circle)
    def draw():
        Game.screen.fill((60, 60, 60, 255))
    
    Game.loop([], [draw, mouse_event])


main()