
from dataclasses import dataclass
from ezdxf.math import Vec2

from profilo import Direzione

@dataclass
class Quota():
    row: int # moltiplicatore offset linea di quota
    p1: Vec2
    p2: Vec2
    direzione: Direzione = Direzione.GIU # direzione dove quotare
    offset: int = 100 # distanza linea di quota

    def get_angle(self) -> int:
        if self.direzione in (Direzione.SX, Direzione.DX):
            return 90
        return 0

    def get_punto_base(self):
        if self.direzione == Direzione.SX:
            return Vec2(self.p2.x-self.offset, self.p2.y)
        if self.direzione == Direzione.GIU:
            return Vec2(self.p1.x, self.p1.y-self.offset)
        if self.direzione == Direzione.DX:
            return Vec2(self.p2.x+self.offset, self.p2.y)
        
if __name__ == '__main__':
    pass