
from dataclasses import dataclass
from ezdxf.math import Vec2
from enum import Enum, auto

class Lato(Enum):
    SX = auto()
    SU = auto()
    DX = auto()
    GIU = auto()

@dataclass
class Quota():
    row: int # moltiplicatore offset linea di quota
    p1: Vec2
    p2: Vec2
    lato: Lato

    def get_angle(self) -> int:
        if self.lato in (Lato.SX, Lato.DX):
            return 90
        return 0

    def get_punto_base(self, offset):
        if self.lato == Lato.SX:
            return Vec2(self.p2.x-offset*self.row, self.p2.y)
        if self.lato == Lato.GIU:
            return Vec2(self.p1.x, self.p1.y-offset*self.row)
        if self.lato == Lato.DX:
            return Vec2(self.p2.x+offset*self.row, self.p2.y)

    def lunghezza_quota(self):
        x1,y1 = self.p1
        x2,y2 = self.p2
        res = ((x2-x1)**2 + (y2-y1)**2)**(1/2) # pitagora
        return res
        
if __name__ == '__main__':
    pass