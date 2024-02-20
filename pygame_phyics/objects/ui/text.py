import pygame
from pygame_phyics.objects.ui import NEWLINE
from pygame_phyics.objects.ui.ui import UI
from pygame_phyics.vector import Vector


class Text(UI):
    """글자를 화면에 나타냄"""
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name, size, color, Font, interval):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        self.Font = Font
        if Font.startswith('./'):
            self.font = pygame.font.Font(Font, size)
        else: 
            self.font = pygame.font.SysFont(Font, size)
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