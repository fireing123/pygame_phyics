import pygame
from pygame_phyics import game, util
from pygame_phyics.event import Event
from pygame_phyics.input import Input
from pygame_phyics.objects.image import ImageObject
from pygame_phyics.objects.ui import NEWLINE
from pygame_phyics.objects.ui.text import Text
from pygame_phyics.objects.ui.ui import UI
from pygame_phyics.timertask import OnceTimerTask, TimerTask


class InputField(UI):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name, scale, color, font, interval, rect):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        self.image = ImageObject(self, surface=rect, type='topleft', follow=True, collide=True)
        self.image.og_image.fill((0, 0, 0, 128))
        self.input_line = ImageObject(self, surface=(5, scale[1]), type="topleft", follow=True)
        self.input_line.og_image.fill((255,255,255, 255))
        self.field = Text(name + '_text', layer, tag + "_text", visible, [0, 0], 0, name, scale[1], color, font, interval)
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
        if self.focused:
            self.input_line.render(surface, camera)
            
    def instantiate(self):
        super().instantiate()
        self.field.instantiate()