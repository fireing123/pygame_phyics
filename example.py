import pygame_engine

pygame_engine.init((1000, 800), "example", "D:/pygame_engine/example/objects/")

@pygame_engine.world("D:/pygame_engine/example/example.json")
def start():
    pygame_engine.scene.brightening()
    def bg():
        pygame_engine.screen.fill((255,255,255))
    pygame_engine.game_loop(funcs=[bg])
    
start()