import pygame
from pygame_phyics import game
from pygame_phyics import Game
from pygame_phyics.vector import Vector
from pygame_phyics import Manger

Game.init((500, 400), "TileMap")

#Game.import_objects("objects/")

@game.world("scene/tilemap.json")
def tilemap():
    tilemapOB = Manger.scene.get_objects("tilemap")[0]
    def start(cls):
        cls.camera = Manger.scene.camera.location

    def event(cls, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k:
                a, b, c = map(int, input().split())
                print(tilemapOB.set_tile((a, b), c))
            if event.key == pygame.K_g:
                a, b = map(int, input().split())
                print(tilemapOB.get_tile((a, b), True))
            if event.key == pygame.K_o:
                print("on")
                Manger.scene.camera.status = 'glitch'
            if event.key == pygame.K_f:
                print("off")
                Manger.scene.camera.status = 'idle'
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
        pass
    return start, event, update



tilemap()