class Collison:
    def __init__(self, gameobject, phyics, other_gameobject, other_phyics):
        self.gameobject = gameobject
        self.phyics = phyics
        self.other_gameobject = other_gameobject # <<<=== self 
        self.other_phyics = other_phyics