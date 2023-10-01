class Input:
    
    key_board = {}
    
    mouse_click = [0, 0, 0]
    
    @classmethod
    def get_key(cls, key_code):
        if cls.key_board.get(key_code) <= 2:
            return True
        return False
    
    @classmethod
    def get_key_down(cls, key_code):
        if cls.key_board.get(key_code) == 2:
            return True
        return False
    
    @classmethod
    def get_key_up(cls, key_code):
        if cls.key_board.get(key_code) == 1:
            return True
        return False
    
    @classmethod
    def get_mouse(cls, bt):
        if cls.mouse_click[bt] <= 2:
            return True
        return False
    
    @classmethod
    def get_mouse_down(cls, bt):
        if cls.mouse_click[bt] == 2:
            return True
        return False
    
    @classmethod
    def get_mouse_up(cls, bt):
        if cls.mouse_click[bt] == 1:
            return True
        return False