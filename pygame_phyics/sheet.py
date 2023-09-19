from pygame import Surface
from pygame import image
import xml.etree.ElementTree as xml

class SurfaceSheet:
    def __init__(self):
        self.image : Surface
    
    @staticmethod
    def load(path):
        root = xml.parse(path)
        sheet = SurfaceSheet()
        sheet.image = image.load(root.attrib['path'])
        sheet.images = {}
        for child in root:
            att = child.attrib
            xywh = map(int, (att['x'], att['y'], att['width'], att['height']))
            sheet.images[att['name']] = SurfaceSheet.get_image(sheet, *xywh)
            
    def get_image(self, x, y, width, height):
        image = Surface((width, height))
        image.fill((158, 165, 147))
        image.set_colorkey((158, 165, 147))
        image.blit(self.image, (0, 0), (x, y, width, height))
        return image