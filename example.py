import pygame_engine

pygame_engine.init((1000, 800), "example", "D:/pygame_engine/example/objects/")

@pygame_engine.world("D:/pygame_engine/example/example.json")
def start():
    pygame_engine.scene.brightening()
    
    pygame_engine.game_loop()
    
start()