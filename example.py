from pygame_phyics.game import Game
from pygame_phyics import DynamicObject
from pygame_phyics.game import world

Game.init((1000, 800), "MyGame")

Game.import_objects("example/objects/")

@world("example/example.json")
def main():
    rect : DynamicObject= Game.scene.get_objects("hello")[0]
    circle = Game.scene.get_objects("llo")[0]
    rect.CreateJoint(4.0, 0.5, circle, (-0.5, -0.5),(-0.5, -0.5))
    def draw():
        Game.screen.fill((60, 60, 60, 255))
    
    Game.loop([], [draw])


main()