"""

기본 오브젝트 모듈
여기서 상속받아 클래스를 만들면 된다

"""

import pygame
import Box2D
from pygame_phyics.manger import Manger
from pygame_phyics import PPM
from pygame_phyics.input import Input
from pygame_phyics.event import Event
from pygame_phyics.vector import Vector
from pygame_phyics.timertask import TimerTask, OnceTimerTask
import pygame_phyics.util as util
import pygame_phyics.game as game
from pygame_phyics.camera import Camera


class Component:
    """기본 함수만 선언해놓음"""
    def on_mouse_enter(self, pos: tuple[int, int]):
        """마우스가 오브젝트(rect) 안에 들어올떄 호출됨

        Args:
            pos (tuple[int, int]): 마우스 위치 (접촉한 위치)
        """
        pass
    def on_mouse_stay(self, pos: tuple[int, int]):
        """마우스가 오브젝트(rect) 에서 들어온 상태일떄 계속 호출됨

        Args:
            pos (tuple[int, int]): 마우스 위치 (접촉한 위치)
        """
        pass
    def on_mouse_exit(self, pos: tuple[int, int]):
        """마우스가 오브젝트(rect) 에서 들어온 상태였다가 나오면 호출됨

        Args:
            pos (tuple[int, int]): 마우스 위치 (접촉한 위치)
        """
        pass
    def update(self):
        """게임 루프시 한번씩 실행됩니다"""
        pass
    def render(self, surface: pygame.Surface, camera: Camera):
        """씬에서 그릴때 실행합니다

        Args:
            surface (pygame.Surface): 프로그램 화면
            camera (Camera): 씬 카메라
        """
        pass
    
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
        
        position = self.object.render_position.rotate_vector(world_position, self.object.angle)

        self.rect = self.image.get_rect(**{self.type: position.xy})
        
        if self.collide:
            self.object.rect = self.rect


    def render(self, surface, camera):
        if self.visible:
            if self.is_follow_camera:
                self.image = pygame.transform.rotate(self.og_image, self.angle + self.object.angle)
            else:
                self.image = pygame.transform.rotate(self.og_image, self.angle + self.object.angle + Manger.scene.camera.angle)
            
            if self.is_follow_camera:
                surface.blit(self.image, self.rect.topleft)
            else:
                surface.blit(self.image, self.image.get_rect(center=camera(self.rect.center)))

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
            anchorA=self.body.transform.position,
            anchorB=body.body.transform.position
        )
        Joint.joints.append(joint)
        return joint

class Object(Component):
    """
    새상에 등록할수있는 가장 기초적인 오브젝트
    save 사용시 주의사항: 매개변수 이름이랑 저장용 변수 이름이랑 이름이 같아야합니다
    """
    
    def __init__(self, name, layer, tag):
        self.name = name
        self.tag = tag
        self.layer = layer

    def delete(self): 
        """씬에서 이 오브젝트를 삭제합니다"""
        Manger.scene.remove(self)
        del self

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
    
    @util.getter
    def render_position(self):
        """y 좌표를 반전시켜줍니다
        pygame 은 화면에 그릴떄 y 선이 아래로 이동할수록 + 라서 
        사용자가 햇갈릴수 있기 떄문에 멥 파일에선 우리가 사용하는 방식으로작성하고
        그릴떄 좌표를 이것으로 사용하시면 됩니다.
        하지만 좌표가 topleft 기준입니다"""
        return Vector(self.position.x, Manger.HEIGHT - self.position.y)


def circle_render(circle, body, surface, camera):
    position = body.transform * circle.pos * PPM
    position = camera((position[0], Manger.HEIGHT - position[1]))
    pygame.draw.circle(surface, (127, 127, 127, 255), [int(
        x) for x in position], int(circle.radius * PPM), 1)
Box2D.b2CircleShape.render = circle_render
def polygon_render(polygon, body, surface, camera):
    vertices = [(body.transform * v) * PPM for v in polygon.vertices]
    vertices = [(v[0], Manger.HEIGHT - v[1]) for v in vertices]
    vertices = [camera(v) for v in vertices]
    pygame.draw.polygon(surface, (127, 127, 127, 255), vertices, 1)
Box2D.b2PolygonShape.render = polygon_render
    
class Phyics(GameObject, Joint):
    """물리오브젝트에 공통점"""
    
    def __init__(self, name: str, tag, visible, layer):
        GameObject.__init__(self, name, tag, visible, layer)
        self.collide_enter = None
    
    def on_collision_enter(self, collision: GameObject):
        """물리 오브젝트가 충돌시 이 함수가 호출됩니다

        Args:
            collision (GameObject): 충돌하는 상대 오브젝트 입니다
        """
        pass
    
    def clean_collision(self):
        """충돌하고 상대 오브젝트 주소를 삭제해 다음 충돌을 받을수 있도록 합니다"""
        self.collide_enter = None
    
    def render(self, surface, camera):
        if self.collide_visible:
            for fixture in self.body.fixtures:
                fixture.shape.render(self.body, surface, camera)
    
    def delete(self):
        """이 오브젝트를 물리 새상과 씬에서 제거합니다"""
        Manger.world.DestroyBody(self.body)
        GameObject.delete(self)
    
    
    @property
    def position(self):
        pos = self.body.transform.position * PPM
        return Vector(pos.x, pos.y)

    
    @position.setter
    def position(self, value: Vector): # value 는 x, y 를 가지는 vector 로
        self.body.transform.position.x = value.x / PPM
        self.body.transform.position.y = value.y / PPM
        
    @property
    def angle(self):
        return self.body.angle * 45

    @angle.setter
    def angle(self, value):
        self.body.angle = value / 45

class StaticObject(Phyics): 
    """정적 물리 오브젝트"""
    def __init__(self, name, tag, visible, layer,
        position, rotate, scale, shape_type, collide_visible):
        super().__init__(name, tag, visible, layer)
        self.collide_visible = collide_visible
        match shape_type:
            case "chain":
                self.shape = Box2D.b2ChainShape(vertices_chain=scale)
            case "circle":
                self.shape = Box2D.b2CircleShape(radius=scale)
            case "edge":
                self.shape = Box2D.b2EdgeShape(vertices=scale)
            case "polygon":
                self.shape = Box2D.b2PolygonShape(vertices=scale)
        self.body : Box2D.b2Body = Manger.world.CreateStaticBody(
            shapes=self.shape
            )
        self.body.userData = self
        self.position = Vector(*position)
        self.angle = rotate
    

class DynamicObject(Phyics):
    """동적 물리 오브젝트"""
    def __init__(self, name, tag, visible, layer,
        position, rotate, scale : tuple | float, shape_type, collide_visible,
        density, friction):
        super().__init__(name, tag, visible, layer)
        self.collide_visible = collide_visible
        self.body : Box2D.b2Body = Manger.world.CreateDynamicBody()
        self.body.userData = self
        self.position = Vector(*position)
        self.angle = rotate
        match shape_type:
            case "chain":
                self.shape = self.body.CreateChainFixture(vertices_chain=scale, density=density, friction=friction)
            case "circle":
                self.shape = self.body.CreateCircleFixture(radius=scale, density=density, friction=friction)
            case "edge":
                self.shape = self.body.CreateEdgeFixture(vertices=scale, density=density, friction=friction)
            case "polygon":
                self.fixture = self.body.CreatePolygonFixture(vertices=scale, density=density, friction=friction)

class UI(GameObject):
    """ui 를 위한 오브젝트"""
    def __init__(self, name: str, tag, visible, layer, position, angle):
        super().__init__(name, tag, visible, layer)
        self.position : Vector = Vector(*position)
        self.angle = angle

NEWLINE = '\n'

class Text(UI):
    """글자를 화면에 나타냄"""
    def __init__(self, name: str, tag, visible, layer, position, angle, size, color, Font, interval):
        super().__init__(name, tag, visible, layer, position, angle)
        self.Font = Font
        self.font = pygame.font.Font(Font, size)
        self.size = size
        self.interval = interval
        self.color = color
        self.text = ""
    
    def get_position(self, __index: int) -> Vector:
        """글자에 index 주소로 접근해서 position 을 0, 0 으로 할때 x,y 좌표를 반환합니디

        Args:
            __index (int): 글자 위치

        Returns:
            Vector: position 을 0, 0 으로 할때 x,y 좌표, 월드 좌표가 아닙니다
        """
        line = self.get_line(__index)
        text = self.text[:__index].split(NEWLINE)[-1]
        x, _ = self.font.size(text)
        y = self.size + self.interval
        y *= line
        return Vector(x-5, -y)

    def get_line(self, __index: int) -> int:
        """글자에 index 주소로 접근해서 이 글자가 어느 라인에 위치한지 찾습니다

        Args:
            __index (int): 글자위치

        Returns:
            int: 라인 번호
        """
        text = self.text[:__index]
        line = text.count(NEWLINE)
        return line

    def render(self, surface : pygame.Surface, camera):
        texts = self.text.split(NEWLINE)
        self.images = [self.font.render(text, True, self.color) for text in texts]
        positions = []
        x, y = self.render_position
        for i in texts:
            positions.append((x, y))
            y += self.size + self.interval
        surface.blits(list(zip(self.images, positions)))

class Button(UI):
    def __init__(self, name: str, tag, visible, layer, position, angle, default, clicked):
        super().__init__(name, tag, visible, layer, position, angle)
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
    

class InputField(UI):
    def __init__(self, name: str, tag, visible, layer, position, angle, scale, color, font, interval, rect):
        super().__init__(name, tag, visible, layer, position, angle)
        self.image = ImageObject(self, surface=rect, type='topleft', follow=True, collide=True)
        self.image.og_image.fill((0, 0, 0, 128))
        self.input_line = ImageObject(self, surface=(5, scale[1]), type="topleft", follow=True)
        self.input_line.og_image.fill((255,255,255, 255))
        
        self.field = Text(name+"field", tag, visible, layer, position, angle, scale[1], color, font, interval)
        self.text = ""
        self.focused = False
        self.editing_pos = 0
        
        self.text_edit = False
        self.text_editing = ""
        self.text_editing_pos = 0
        
        self.backspace = False
        self.stay = False
        self.timertask = TimerTask(600, self.toggle_bar)
        self.backtime = TimerTask(40, lambda :self.focus_cut(1))
        self.wait_backspace = OnceTimerTask(350, self.toggle_backspace)
        
        self.input_event = Event()
        game.event_event.add_lisner(self.inputfield_event)
        
    def bar_reset(self):
        """커서에 깜빡거림에 주기를 초기화합니다
        """
        self.timertask.reset()
        self.input_line.visible = True
        
    def toggle_bar(self):
        """커서를 토글로 껏다킵니다
        """
        self.input_line.visible = not self.input_line.visible
    
    def toggle_backspace(self):
        """연속 지우기를 토글로 제어합니다
        """
        self.backspace = not self.backspace
    
    def insert(self, index: int, value: str):
        """index 위치에 value 를 삽입합니다

        Args:
            index (int): 위치
            value (str): 삽입할 글자
        """
        self.text = util.string_insert(self.text, value, index)
    
    def cut(self, range: tuple[int, int]):
        """일정 범위에 글자를 잘라냅니다

        Args:
            range (tuple[int, int]): 잘라낼 범위
        """
        self.text = util.string_cut(self.text, range)
    
    def focus_insert(self, value: str):
        """커서를 기준으로 글자를 삽입합니다

        Args:
            value (str): 삽입할 글자
        """
        self.insert(self.editing_pos, value)
        self.set_edit_pos(len(value), add=True)
    
    def focus_cut(self, size: int):
        """커서를 기준으로 글자를 잘라냅니다

        Args:
            size (int): 커서로부터 이만큼 잘라냅니다
        """
        self.cut((self.editing_pos-size, self.editing_pos))
        self.set_edit_pos(size, sub=True)
        
    def set_edit_pos(self, pos: int, **kwargs):
        """커서에 위치를 변경합니다
        add 키워드는 bool 로 True 일떄 인수로 받은 pos를 더합니다
        sub 키워드는 bool 로 True 일떄 인수로 받은 pos를 뺍니다

        Args:
            pos (int): 커서 위치, 또는 연산할 값
        """
        if kwargs.get("add"):
            pos += self.editing_pos
        elif kwargs.get("sub"):
            pos = self.editing_pos - pos
        length = len(self.text+self.text_editing)
        if 0 >= pos:
            self.editing_pos = 0
        elif pos > length:
            self.editing_pos = length
        else:
            self.editing_pos = pos
    
    def on_mouse_enter(self, pos):
        self.stay = True
    
    def on_mouse_stay(self, pos):
        if Input.get_mouse_down(0):
            self.focused = True
    
    def on_mouse_exit(self, pos):
        self.stay = False
    
    def update(self):
        if self.focused:
            if Input.get_key_down(pygame.K_BACKSPACE):
                self.wait_backspace.reset()
                if len(self.text) > 0 and self.editing_pos > 0:
                    self.focus_cut(1)
                    self.bar_reset()   

            elif Input.get_key_down(pygame.K_DELETE):
                self.cut((self.editing_pos, self.editing_pos+1))

            elif Input.get_key_down(pygame.K_LEFT):
                self.set_edit_pos(1, sub=True)
                self.bar_reset()  

            elif Input.get_key_down(pygame.K_RIGHT):
                self.set_edit_pos(1, add=True)
                self.bar_reset()  

            elif Input.get_key_down(13):
                self.focus_insert(NEWLINE)

            elif Input.get_key_down(pygame.K_KP_ENTER):
                self.focused = False
                self.input_event.invoke(self.text)

            elif Input.get_key(pygame.K_BACKSPACE):
                self.wait_backspace.run_periodic_task()

            elif Input.get_key_up(pygame.K_BACKSPACE):
                self.backspace = False

            if self.backspace:
                self.backtime.run_periodic_task()

        self.image.update()
        
        if not self.stay and Input.get_mouse_down(0):
            self.focused = False
        
        self.field.text = self.text + self.text_editing
        edit_text_pos = self.editing_pos + len(self.text_editing)
        
        if self.focused:
            self.timertask.run_periodic_task()
            
            if self.input_line.visible:
                self.input_line.position = self.field.get_position(edit_text_pos)
        
        self.input_line.update()
    
    def inputfield_event(self, event):
        """입력 필드에 이벤트

        Args:
            event (event): pygame 에 이벤트입니다_
        """
        if self.focused:
            if event.type == pygame.TEXTEDITING:
                self.text_edit = True
                self.text_editing = event.text
                self.text_editing_pos = event.start
                self.bar_reset()    
            elif event.type == pygame.TEXTINPUT:
                self.text_edit = False
                self.text_editing = ""
                self.focus_insert(event.text)
                self.bar_reset()    

    def render(self, surface, camera):
        self.image.render(surface, camera)
        self.field.render(surface, camera)
        if self.focused:
            self.input_line.render(surface, camera)

class TileMap(GameObject):
    def __init__(self, name: str, tag, visible, layer, tiles: list[dict[int, dict[int, str]]], data: dict[str, dict]):
        super().__init__(name, tag, visible, layer)
        self.tiles = tiles
        self.size = data['size']
        self.canvas = {key: pygame.image.load(path) for key, path in data['canvas'].items()}
        self.str_canvas = data['canvas'].values()
        
    @util.getter
    def data(self):
        return {
            "size": self.size,
            "canvas": self.str_canvas
        }
        
    def set_tile(self, xy, value):
        match xy:
            case n if n[0] >= 0 and n[1] >= 0:
                y = self.tiles[0].get(n[1])
                if y != None:
                    y[str(n[0])] = value
                else:
                    y = {}[str(n[0])] = value
            case n if n[0] < 0 and n[1] >= 0:
                y = self.tiles[0].get(n[1])
                if y != None:
                    y[str(-n[0])] = value
                else:
                    y = {}[str(-n[0])] = value
            case n if n[0] < 0 and n[1] < 0:
                y = self.tiles[0].get(-n[1])
                if y != None:
                    y[str(-n[0])] = value
                else:
                    y = {}[str(n[0])] = value
            case n if n[0] >= 0 and n[1] < 0:
                y = self.tiles[0].get(-n[1])
                if y != None:
                    y[str(n[0])] = value
                else:
                    y = {}[str(n[0])] = value
        
    def get_tile(self, xy):
        match xy:
            case n if n[0] >= 0 and n[1] >= 0:
                return self.tiles[0].get(str(n[1]), {}).get(str(n[0]))
            case n if n[0] < 0 and n[1] >= 0:
                return self.tiles[1].get(str(n[1]), {}).get(str(-n[0]))
            case n if n[0] < 0 and n[1] < 0:
                return self.tiles[2].get(str(-n[1]), {}).get(str(-n[0]))
            case n if n[0] >= 0 and n[1] < 0:
                return self.tiles[3].get(str(-n[1]), {}).get(str(n[0]))
    
    def get_tile_image(self, n):
        return self.canvas[n]
    
    def render(self, surface, camera):
        HALF_WIDTH = Manger.WIDTH / (self.size * 2)
        HALF_HEIGHT = Manger.HEIGHT / (self.size * 2)
        tile_camera = camera.vector.div_float(self.size)
        xrange = int(tile_camera.x - HALF_WIDTH), int(tile_camera.x + HALF_WIDTH) + 1
        yrange = int(tile_camera.y - HALF_HEIGHT), int(tile_camera.y + HALF_HEIGHT) + 1
        for y in range(*yrange):
            for x in range(*xrange):
                tile_n = self.get_tile((x, y))
                if tile_n != None:
                    image = self.get_tile_image(tile_n)
                    cx = (HALF_WIDTH + x) * self.size - camera.x
                    cy = (HALF_HEIGHT - y) * self.size + camera.y
                    surface.blit(image, (cx, cy))