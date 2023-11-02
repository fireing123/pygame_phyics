class Input:
    """키보드나 마우스의 입력을 확인합니다"""
    key_board = {}
    
    mouse_click = [0, 0, 0]
    
    @classmethod
    def get_key(cls, key_code):
        """입력을 받는지 확인함니다"""
        
        if cls.key_board.get(key_code, 0) <= 2:
            return True
        return False
    
    @classmethod
    def get_key_down(cls, key_code):
        """이 키가 눌리는 순간인지 확인합니다"""
        
        if cls.key_board.get(key_code, 0) == 2:
            return True
        return False
    
    @classmethod
    def get_key_up(cls, key_code):
        """이 키가 더이상 입력을 받지 않는지 확인합니다"""
        
        if cls.key_board.get(key_code, 0) == 1:
            return True
        return False
    
    @classmethod
    def get_mouse(cls, button):
        """클릭중인지 확인합니다"""
        
        if cls.mouse_click[button] <= 2:
            return True
        return False
    
    @classmethod
    def get_mouse_down(cls, button):
        """클릭 하는 순간인지 확인합니다"""
        
        if cls.mouse_click[button] == 2:
            return True
        return False
    
    @classmethod
    def get_mouse_up(cls, button):
        """더이상 클릭을 하지 않는지 확인합니다"""
        if cls.mouse_click[button] == 1:
            return True
        return False