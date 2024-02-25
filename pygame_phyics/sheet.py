from pygame import Surface
from pygame import image
import xml.etree.ElementTree as xml

class SurfaceSheet:
    def __init__(self, name, path):
        self.name = name
        root = xml.parse(path)
        self.image = image.load(root.attrib['path'])
        self.images = []
        for child in root:
            att = child.attrib
            xywh = map(int, (att['x'], att['y'], att['width'], att['height']))
            self.images.append(self.image.subsurface(xywh))
    
class TileSheet:
    def __init__(self, name, path, size):
        self.name = name
        self.size = size
        self.image = image.load(path)
        self.surfaces = []
        x, y = self.image.get_size()
        fx = 0
        fy = 0
        for i in range(int(y / size)):
            for j in range(int(x / size)):
                self.surfaces.append(self.image.subsurface((fx, fy, size, size)))
                fx += size
            fy += size
            fx = 0