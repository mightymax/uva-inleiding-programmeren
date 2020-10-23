class Keyboard:
    def __init__(self):
        self.keys = {}
    
    def key_down(self, key):
        self.keys[key] = True
    
    def key_up(self, key):
        self.keys[key] = False
    
    def is_down(self, key):
        if key in self.keys:
            return self.keys[key]
        return False

class PosRad:
    def __init__(self, x, y, rad):
        self.x = x
        self.y = y
        self.rad = rad

    def is_in_collision(self, p2):
        dx = self.x-p2.x
        dy = self.y-p2.y
        sr = self.rad+p2.rad
        return dx*dx+dy*dy<sr*sr
