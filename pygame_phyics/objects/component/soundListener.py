from pygame_phyics.objects.component import Component


class SoundListener(Component):
    """오직 한객체만 존재해야함"""
    listener = None

    def __init__(self, object) -> None:
        self.object = object
        if SoundListener.listener != None:
            raise ValueError("이미 SoundListener 컴포넌트는 존재합니다")
        SoundListener.listener = self