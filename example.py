from pygame_engine.game import Game
from pygame_engine.game import world

Game.init((1000, 800), "MyGame")

Game.import_objects("example/objects/")

@world("example/example.json")
def main():

    def draw():
        Game.screen.fill((60, 60, 60, 255))
    
    Game.loop([], [draw])


main()