from pygame_phyics import Manger
from pygame_phyics.timertask import TimerTask

class Animation:
    def __init__(self, tick, image_object, **kwargs):
        self.object = image_object
        self.period = TimerTask(tick)
        self.index = 0
        if  kwargs.get('sheet', None) != None:
            self.sheet = Manger.surface_sheet[kwargs['sheet']]
            if kwargs.get('range', None) != None:
                frist, last = kwargs['range']
                self.images = self.sheet.images[frist:last]
            else:
                raise ValueError("범위를 설정해야함 (int, int) 튜플형식으로 재공")
        else:
            raise ValueError("키워드가 적절하지 않습니다. sheet 를 사용하면 sheet 키워드에 사용하는 시트에 이름을 작성하세요, xml 문서를 이용한 이미지의 집합을 사용하시면 \'xml\'를 작성하세요")
        self.len = len(self.images)
        
    def update(self):
        if self.period.run_periodic_task():
            self.change_image()

    def change_image(self):
        self.object.og_image = self.images[self.index]
        self.index += 1
        if self.index == self.len:
            self.index = 0