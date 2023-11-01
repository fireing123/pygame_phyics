import inspect
import pygame
from pygame_phyics.util import jsave
from pygame_phyics.manger import Manger

def save(layers, export_path, **kwargs):
    kwargs['camera'] = list(Manger.scene.camera.vector.xy)
    saved_dict = {
        'setting':kwargs,
        'objs':{
            
        }
    }

    objs = {}
    for layer in layers:
        for obj in layer:
            prargs = {}
            parameters = list(inspect.signature(obj.__class__).parameters.keys())
            for parameter in parameters:
                value = getattr(obj, parameter, None)
                if value == None:
                    raise ValueError(f"{obj.__class__.__name__}는 {parameter} 속성이 존재하지 않습니다")
                if hasattr(value, "isiter"):
                    prargs[parameter] = list(value)
                elif isinstance(value, pygame.rect.Rect):
                    prargs[parameter] = [value.width, value.height]
                else:
                    prargs[parameter] = value
            class_name = obj.__class__.__name__
            ishas_class = objs.get(class_name)
            if ishas_class == None:
                objs[class_name] = [prargs]
            else:
                objs[class_name].append(prargs)
    saved_dict['objs'] = objs
    
    jsave(saved_dict, export_path)