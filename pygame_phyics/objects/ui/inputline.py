from pygame_phyics.objects.ui.ui import UI
from pygame_phyics.objects.image import ImageObject

class InputLine(UI):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name, y):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        
        image = ImageObject(self, surface=(5, y), type="topleft", follow=True)
        image.og_image.fill((255,255,255, 255))
        self.components.append(image)