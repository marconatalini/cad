from dim import Quota, Lato
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from ezdxf.math import Vec2

class Direzione(Enum):
    SU = 90
    DX = 0
    GIU = -90
    SX = -180
    VERTICALE = 90
    ORIZZONTALE = 0

@dataclass
class Articolo():
    codice: str
    larghezza: int

@dataclass
class Profilo():
    '''
    Definisce un pezzo di profilo alluminio
    il punto di partenza è definito (0,0)
    '''
    articolo: Articolo
    lunghezza: int
    punto_partenza: tuple # (x,y)
    direzione: Direzione
    angolo_inizio: int = 90
    angolo_fine: int = 90

    def coords(self):
        '''
        Definisce i 4 punti in senso orario per disegnare la polyline del profilo
        Il profilo è considerato orizzontale, punto di partenza è in alto a SX
        '''
        larghezza = self.articolo.larghezza
        coords = [(0, 0), (self.lunghezza, 0)]
        if self.angolo_fine == 90:
            coords.append((self.lunghezza, -larghezza))
        if self.angolo_fine == 45:
            coords.append((self.lunghezza - larghezza, -larghezza))
        if self.angolo_inizio == 90:
            coords.append((0, -larghezza))
        if self.angolo_inizio == 45:
            coords.append((larghezza, -larghezza))
        return coords

class Struttura(ABC):
    '''Struttura perimetrale supporto pannello'''

    def __init__(self, base: int, altezza: int) -> None:
        '''Base anta alluminio, Altezza anta alluminio'''

class Struttura_1(Struttura):
    '''Struttura perimetrale pannello a sormonto normale'''

    def __init__(self, base: int, altezza: int) -> None:

        art = Articolo('AP31110', 31)

        self.base = base -8
        self.altezza = altezza

        p_sx = Profilo(art, self.altezza, (0, 0), Direzione.SU, 45, 45)
        p_su = Profilo(art, self.base, (0, self.altezza), Direzione.DX, 45, 45)
        p_dx = Profilo(art, self.altezza, (self.base, self.altezza), Direzione.GIU, 45, 45)
        p_giu = Profilo(art, self.base, (self.base, 0), Direzione.SX, 45, 45)
        self.profili = [p_sx, p_su, p_dx, p_giu]

    def quote(self):
        result = []
        larg_profilo = self.profili[0].articolo.larghezza
        result.append(Quota(2, Vec2(larg_profilo, larg_profilo), Vec2(larg_profilo, self.altezza-larg_profilo), Lato.SX))
        result.append(Quota(2, Vec2(larg_profilo, larg_profilo), Vec2(self.base-larg_profilo, larg_profilo), Lato.GIU))        
        result.append(Quota(3, Vec2(0, 0), Vec2(0, self.altezza), Lato.SX))        
        result.append(Quota(3, Vec2(0, 0), Vec2(self.base, 0), Lato.GIU))        

        return result


if __name__ == '__main__':
    pass