from pygame_phyics.objects.ui.ui import UI
from pygame_phyics.event import Event
from pygame_phyics.input import Input
from pygame_phyics.objects.image import ImageObject


class Button(UI):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name, default, clicked):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        self.default = ImageObject(self, default, follow=True, collide=True)
        self.clicked = ImageObject(self, clicked, follow=True, collide=True)
        self.image = self.default
        self.rect = self.image.rect
        self.is_click = Event()
    
    def on_mouse_stay(self, pos):
        if Input.get_mouse_down(0):
            self.is_click.invoke() 
            self.image = self.clicked
        elif Input.get_mouse_up(0):
            self.image = self.default
    
    def update(self):
        self.image.update()
        
    def render(self, surface, camera):
        self.image.render(surface, camera)