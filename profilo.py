
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto

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

        p1 = Profilo(art, self.altezza, (0, 0), Direzione.SU, 45, 45)
        p2 = Profilo(art, self.base, (0, self.altezza), Direzione.DX, 45, 45)
        p3 = Profilo(art, self.altezza, (self.base, self.altezza), Direzione.GIU, 45, 45)
        p4 = Profilo(art, self.base, (self.base, 0), Direzione.SX, 45, 45)
        self.profili = [p1, p2, p3, p4]

    def quote(self):
        return []


if __name__ == '__main__':
    pass