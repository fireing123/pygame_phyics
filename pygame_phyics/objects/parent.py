

from pygame_phyics.objects.object import Object
from pygame_phyics.location import Parent


class ParentObject(Object):
    def __init__(self):
        super().__init__("parent", 0, "top")
        self.location = Parent()
        
    def set_parent(self):
        pass