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
import pygame_phyics.game as game

def rotate_point_around_origin(x, y, angle_degrees):
    angle_radians = math.radians(angle_degrees)
    new_x = x * math.cos(angle_radians) - y * math.sin(angle_radians)
    new_y = x * math.sin(angle_radians) + y * math.cos(angle_radians)
    return new_x, new_y

def rotate_point_b_around_a(a, b, angle_degrees):
    b_relative_to_a = (b[0] - a[0], b[1] - a[1])
    rotated_b_relative_to_a = rotate_point_around_origin(b_relative_to_a[0], b_relative_to_a[1], angle_degrees)
    rotated_b = (rotated_b_relative_to_a[0] + a[0], rotated_b_relative_to_a[1] + a[1])
    return rotated_b

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
    
    def __init__(self, object, image, position=(0, 0), angle=0):
        self.object = object
        self.og_image = pygame.image.load(image)
        self.image = self.og_image
        self.rect = self.image.get_rect()
        self.position = position
        self.angle = angle
    
    def update(self):
        """이미지에 위치 각도 등을 조정함"""
        
        position = rotate_point_b_around_a([obj_pos * PPM for obj_pos in self.object.position], [obj * PPM + pos for obj, pos in zip(self.object.position, self.position)], self.object.angle)
        self.image = pygame.transform.rotate(self.og_image, self.angle + self.object.angle)
        self.rect = self.image.get_rect(center=position)
        self.object.rect = self.rect

    def render(self, surface, camera):
        self.rect.centery = surface.get_size()[1] - self.rect.centery
        self.rect.center = self.rect.center[0] - camera.x, self.rect.center[1] - camera.y
        surface.blit(self.image, self.rect)

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

class object(Component):
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

class GameObject(object):
    """마우스 충돌 연산가능함"""
    
    def __init__(self, name: str, tag, visible, layer):
        super().__init__(name, layer, tag)
        self.visible = visible
        self.rect = None
        self.collide = 'out'
    
def circle_render(circle, body, surface, camera):
    position = body.transform * circle.pos * PPM
    position = (position[0] - camera[0], surface.get_size()[1] - position[1] - camera[1])
    pygame.draw.circle(surface, (127, 127, 127, 255), [int(
        x) for x in position], int(circle.radius * PPM), 1)
Box2D.b2CircleShape.render = circle_render

def polygon_render(polygon, body, surface, camera):
    vertices = [(body.transform * v) * PPM for v in polygon.vertices]
    vertices = [(v[0], surface.get_size()[1] - v[1]) for v in vertices]
    vertices = [(v[0] - camera[0], v[1] - camera[1]) for v in vertices]
    pygame.draw.polygon(surface, (127, 127, 127, 255), vertices, 1)
Box2D.b2PolygonShape.render = polygon_render
    
class Phyics(GameObject, Joint):
    """물리오브젝트에 공통점"""
    
    def delete(self):
        Manger.world.DestroyBody(self.body)
        GameObject.delete(self)
    
    @property
    def position(self):
        return self.body.transform.position
    
    @position.getter
    def position(self):
        return self.body.transform.position
    
    @position.setter
    def position(self, value):
        self.body.transform.position
    
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
            position=position,
            angle=rotate,
            shapes=self.shape
            )
    
    def render(self, surface, camera):
        if self.collid_visible:
            for fixture in self.body.fixtures:
                fixture.shape.render(self.body, surface, camera)

class DynamicObject(Phyics):
    def __init__(self, name, tag, visible, layer,
        position, rotate, scale : tuple | float, shape_type, collid_visible,
        density, friction):
        super().__init__(name, tag, visible, layer)
        self.collid_visible = collid_visible
        self.body : Box2D.b2Body = Manger.world.CreateDynamicBody(
            position=position,
            angle=rotate
        )
        match shape_type:
            case "chain":
                pass
            case "circle":
                self.shape = self.body.CreateCircleFixture(radius=scale, density=density, friction=friction)
            case "edge":
                pass
            case "polygon":
                self.fixture = self.body.CreatePolygonFixture(vertices=scale, density=density, friction=friction)
    
    def render(self, surface, camera):
        if self.collid_visible:
            for fixture in self.body.fixtures:
                fixture.shape.render(self.body, surface, camera)

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
        x = self.position[0] * PPM
        y = self.position[1] * PPM
        x -= camera[0]
        y -= camera[1]
        self.positions = []
        for i in texts:
            self.positions.append((x, y))
            y += self.size + self.interval
        surface.blits(list(zip(self.images, self.positions)))

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
        self.image = pygame.Surface(rect)
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect(topleft=[pos * PPM for pos in position])
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
        surface.blit(self.image, self.rect)
        self.field.render(surface, camera)