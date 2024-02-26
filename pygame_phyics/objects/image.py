import pygame
from pygame_phyics.objects.component import Component
from pygame_phyics.vector import Vector
from pygame_phyics.manger import Manger

class ImageObject(Component):
    """이미지에 위치, 각도를 관리하고 화면에 나타낸다
    씬에서 그려지는 오브젝트가 아닙니다
    """
    
    def __init__(self, object, image=None, position=(0, 0), angle=0, **kwargs):
        self.object = object
        self.visible = True
        self.og_image = pygame.image.load(image) if kwargs.get('surface') == None else pygame.Surface(kwargs['surface'], pygame.SRCALPHA)
        self.collide = kwargs.get("collide", False)
        self.is_follow_camera = kwargs.get("follow", False)
        self.image = self.og_image
        self.rect = self.image.get_rect()
        self.position = Vector(*position)
        self.angle = angle
        self.type = 'center' if kwargs.get('type') == None else kwargs['type']
    
    def update(self):
        obj_self = list(zip(self.object.render_position.xy, self.position.xy))
        obj_self_ys = obj_self[1]
        
        world_position = Vector(sum(obj_self[0]), obj_self_ys[0] - obj_self_ys[1])
        
        position = self.object.render_position.rotate_vector(world_position, self.object.location.rotation)

        self.rect = self.image.get_rect(**{self.type: position.xy})
        
        if self.collide:
            self.object.rect = self.rect


    def render(self, surface, camera):
        if self.visible:
            if self.is_follow_camera:
                self.image = pygame.transform.rotate(self.og_image, self.angle + self.object.location.rotation)
            else:
                self.image = pygame.transform.rotate(self.og_image, self.angle + self.object.location.rotation + Manger.scene.camera.location.rotation)
            
            if self.is_follow_camera:
                surface.blit(self.image, self.rect.topleft)
            else:
                surface.blit(self.image, self.image.get_rect(center=camera(self.rect.center)))