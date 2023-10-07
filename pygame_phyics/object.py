"""

기본 오브젝트 모듈
여기서 상속받아 클래스를 만들면 된다

"""

import math
import pygame
import Box2D.b2 as b2
import Box2D
from pygame_phyics.manger import Manger
from pygame_phyics import PPM
from pygame_phyics.input import Input
from pygame_phyics.event import Event
from pygame_phyics.error import ImmutableAttributeError
import pygame_phyics.game as game
import math

def rotate_point(point_a, point_b, angle_degrees):
    angle_radians = math.radians(360 - angle_degrees)
    x_b, y_b = point_b
    x_a, y_a = point_a
    x_b_rotated = (x_b - x_a) * math.cos(angle_radians) - (y_b - y_a) * math.sin(angle_radians) + x_a
    y_b_rotated = (x_b - x_a) * math.sin(angle_radians) + (y_b - y_a) * math.cos(angle_radians) + y_a
    return x_b_rotated, y_b_rotated

class Component:
    def on_mouse_enter(self, pos):
        pass
    def on_mouse_stay(self, pos):
        pass
    def on_mouse_exit(self, pos):
        pass
    def update(self):
        pass
    def render(self, surface, camera):
        pass
    
class ImageObject(Component):
    """오브젝트가 아님 오브젝트에 속성으로 사용"""
    
    def __init__(self, object, image=None, position=(0, 0), angle=0, **kwargs):
        self.object = object
        self.og_image = pygame.image.load(image) if kwargs.get('surface') == None else pygame.Surface(kwargs['surface'])
        self.image = self.og_image
        self.rect = self.image.get_rect()
        self.position = position
        self.angle = angle
        self.type = 'center' if kwargs.get('type') == None else kwargs['type']
    
    def update(self):
        """이미지에 위치 각도 등을 조정함"""
        position = rotate_point(self.object.render_position, [obj - pos for obj, pos in zip(self.object.render_position, self.position)], self.object.angle)
        self.image = pygame.transform.rotate(self.og_image, self.angle + self.object.angle)
        self.rect = self.image.get_rect()
        setattr(self.rect, self.type, position)
        self.object.rect = self.rect

    def render(self, surface, camera):
        surface.blit(self.image, camera(self.rect.topleft))

class Joint:
    """물리 연산의 연결 담당"""
    joints = []
    
    def create_joint(self, frequency_hz, damping_ratio, body):
        """자기 자신과 인수로 받은 body 를 연결합니다"""
        
        joint = Manger.world.CreateDistanceJoint(
            frequencyHz=frequency_hz,
            dampingRatio=damping_ratio,
            bodyA=self.body,
            bodyB=body.body,
            anchorA=self.position,
            anchorB=body.body.transform.position
        )
        Joint.joints.append(joint)
        return joint

class Object(Component):
    """새상에 등록할수있는 가장 기초적인 오브젝트"""
    
    def __init__(self, name, layer, tag):
        self.name = name
        self.tag = tag
        self.layer = layer

    def delete(self): 
        Manger.scene.remove(self)

    @staticmethod
    def instantiate(object):
        Manger.scene.add(object)

class GameObject(Object):
    """마우스 충돌 연산가능함"""
    
    def __init__(self, name: str, tag, visible, layer):
        super().__init__(name, layer, tag)
        self.visible = visible
        self.rect = None
        self.collide = 'out'
    
    @property
    def render_position(self):
        return self.position
    
    @render_position.getter
    def render_position(self):
        return self.position[0], Manger.HEIGHT - self.position[1]
    
    @render_position.setter
    def render_position(self, value):
        raise ImmutableAttributeError(__class__, "rander_position")
    
def circle_render(circle, body, surface, camera):
    position = body.transform * circle.pos * PPM
    position = (position[0] - camera[0], Manger.HEIGHT - position[1] - camera[1])
    pygame.draw.circle(surface, (127, 127, 127, 255), [int(
        x) for x in position], int(circle.radius * PPM), 1)
Box2D.b2CircleShape.render = circle_render

def polygon_render(polygon, body, surface, camera):
    vertices = [(body.transform * v) * PPM for v in polygon.vertices]
    vertices = [(v[0], Manger.HEIGHT - v[1]) for v in vertices]
    vertices = [(v[0] - camera[0], v[1] - camera[1]) for v in vertices]
    pygame.draw.polygon(surface, (127, 127, 127, 255), vertices, 1)
Box2D.b2PolygonShape.render = polygon_render
    
class Phyics(GameObject, Joint):
    """물리오브젝트에 공통점"""
    
    def render(self, surface, camera):
        if self.collid_visible:
            for fixture in self.body.fixtures:
                fixture.shape.render(self.body, surface, camera)
    
    def delete(self):
        Manger.world.DestroyBody(self.body)
        GameObject.delete(self)
    
    @property
    def position(self):
        return self.body.transform.position
    
    @position.getter
    def position(self):
        return self.body.transform.position * PPM
    
    @position.setter
    def position(self, value):
        self.body.transform.position = [v / PPM for v in value]
        
    @property
    def angle(self):
        return self.body.angle
    
    @angle.getter
    def angle(self):
        return self.body.angle * 45
    
    @angle.setter
    def angle(self, value):
        self.body.angle = value / 45
          
class StaticObject(Phyics): 
    def __init__(self, name, tag, visible, layer,
        position, rotate, scale : tuple | float, shape_type, collid_visible):
        super().__init__(name, tag, visible, layer)
        self.collid_visible = collid_visible
        match shape_type:
            case "chain":
                self.shape = Box2D.b2ChainShape()
            case "circle":
                self.shape = Box2D.b2CircleShape()
            case "edge":
                self.shape = Box2D.b2EdgeShape(vertices=scale)
            case "polygon":
                self.shape = Box2D.b2PolygonShape(vertices=scale)
        self.body : Box2D.b2Body = Manger.world.CreateStaticBody(
            shapes=self.shape
            )
        self.position = position
        self.angle = rotate
    

class DynamicObject(Phyics):
    def __init__(self, name, tag, visible, layer,
        position, rotate, scale : tuple | float, shape_type, collid_visible,
        density, friction):
        super().__init__(name, tag, visible, layer)
        self.collid_visible = collid_visible
        self.body : Box2D.b2Body = Manger.world.CreateDynamicBody()
        self.position = position
        self.angle = rotate
        match shape_type:
            case "chain":
                pass
            case "circle":
                self.shape = self.body.CreateCircleFixture(radius=scale, density=density, friction=friction)
            case "edge":
                pass
            case "polygon":
                self.fixture = self.body.CreatePolygonFixture(vertices=scale, density=density, friction=friction)

class UI(GameObject):
    def __init__(self, name: str, tag, visible, layer, position, angle):
        super().__init__(name, tag, visible, layer)
        self.position = position
        self.angle = angle

class Text(UI):
    def __init__(self, name: str, tag, visible, layer, position, angle, size, color, Font, interval):
        super().__init__(name, tag, visible, layer, position, angle)
        self.font = pygame.font.Font(Font, size)
        self.size = size
        self.interval = interval
        self.color = color
        self.text = ""
    
    def render(self, surface : pygame.Surface, camera):
        texts = self.text.split('\n')
        self.images = [self.font.render(text, True, self.color) for text in texts]
        x, y = camera(self.render_position)
        positions = []
        for i in texts:
            positions.append((x, y))
            y += self.size + self.interval
        surface.blits(list(zip(self.images, positions)))

class Button(UI):
    def __init__(self, name: str, tag, visible, layer, position, angle, default, clicked):
        super().__init__(name, tag, visible, layer, position, angle)
        self.default = ImageObject(self, default)
        self.clicked = ImageObject(self, clicked)
        self.image = self.default
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
    
   
class InputField(UI):
    def __init__(self, name: str, tag, visible, layer, position, angle, scale, color, font, interval, rect):
        super().__init__(name, tag, visible, layer, position, angle)
        self.image = ImageObject(self, surface=rect, type='topleft')
        self.image.og_image.fill((0, 0, 0, 0))
        self.field = Text(name+"field", tag, visible, layer, position, angle, scale[1], color, font, interval)
        self.text = ""
        self.focused = False
        self.editing_pos = 0
        self.text_edit = False
        self.text_editing = ""
        self.text_editing_pos = 0
        self.stay = False
        self.input_event = Event()
        self._last_update = 0
        self._update = 600
        game.event_event.add_lisner(self.inputfield_event)
        
    def on_mouse_enter(self, pos):
        self.stay = True
    
    def on_mouse_stay(self, pos):
        if Input.get_mouse_down(0):
            self.focused = True
    
    def on_mouse_exit(self, pos):
        self.stay = False
    
    def update(self):
        self.image.update()
        if not self.stay and Input.get_mouse_down(0):
            self.focused = False
        self.field.text = self.text + self.text_editing
        edit_text_pos = self.editing_pos + len(self.text_editing)
        if self.focused:
            if not pygame.time.get_ticks() - self._last_update > self._update:
                self.field.text = self.field.text[:edit_text_pos] + "|" + self.field.text[edit_text_pos:]
            if pygame.time.get_ticks() - self._last_update > self._update*2:
                self._last_update = pygame.time.get_ticks()
    
    def inputfield_event(self, event):
        if self.focused:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if len(self.text) > 0 and self.editing_pos > 0:
                        self.text = self.text[:self.editing_pos-1] + self.text[self.editing_pos:]
                        self.editing_pos = max(0, self.editing_pos - 1)
                elif event.key == pygame.K_DELETE:
                    self.text = self.text[:self.editing_pos] + self.text[self.editing_pos+1:]
                elif event.key == pygame.K_LEFT:
                    self.editing_pos = max(0, self.editing_pos - 1)
                elif event.key == pygame.K_RIGHT:
                    self.editing_pos = min(
                        len(self.text), self.editing_pos + 1
                    )
                elif event.key == 13:
                    self.text += '\n'
                    self.editing_pos += 1
                elif event.key == pygame.K_KP_ENTER:
                    self.focused = False
                    self.input_event.invoke()
            elif event.type == pygame.TEXTEDITING:
                self.text_edit = True
                self.text_editing = event.text
                self.text_editing_pos = event.start
                self._last_update = pygame.time.get_ticks()
            elif event.type == pygame.TEXTINPUT:
                self.text_edit = False
                self.text_editing = ""
                self.text = self.text[:self.editing_pos] + event.text + self.text[self.editing_pos:]
                self.editing_pos += len(event.text)
                self._last_update = pygame.time.get_ticks()

            

    def render(self, surface, camera):
        self.image.render(surface, camera)
        self.field.render(surface, camera)