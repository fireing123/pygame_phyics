import pygame
from pygame_phyics.objects.component import Component
from pygame_phyics.objects.gameobject import GameObject
from pygame_phyics.manger import Manger

class ImageObject(Component):
    """이미지에 위치, 각도를 관리하고 화면에 나타낸다
    씬에서 그려지는 오브젝트가 아닙니다
    """
    
    def __init__(self, object, image=None, **kwargs):
        self.object: GameObject = object
        self.visible = True
        self.og_image = pygame.image.load(image) if kwargs.get('surface') == None else pygame.Surface(kwargs['surface'], pygame.SRCALPHA)
        self.collide = kwargs.get("collide", False)
        self.camera_staticable = kwargs.get("follow", False)
        self.image = self.og_image
        self.rect = self.image.get_rect()
        self.type = 'center' if kwargs.get('type') == None else kwargs['type']
    
    def update(self):
        self.rect = self.image.get_rect(**{self.type: self.object.render_position})
        
        if self.collide:
            self.object.rect = self.rect


    def render(self, surface, camera):
        if self.visible:
            if self.camera_staticable:
                self.image = pygame.transform.rotate(self.og_image, self.object.location.world_rotation)
            else:
                self.image = pygame.transform.rotate(self.og_image, self.object.location.world_rotation + Manger.scene.camera.location.world_rotation)
            
            if self.camera_staticable:
                surface.blit(self.image, self.rect.topleft)
            else:
                surface.blit(self.image, self.image.get_rect(center=camera(self.rect.center)))