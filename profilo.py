from dim import Quota, Lato
from abc import ABC
from dataclasses import dataclass
from typing import List, Union
from enum import Enum
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

catalogo = {
    'AP31110' : Articolo('AP31110', 31),
    'AP42110' : Articolo('AP42110', 42),
}

class Profilo():
    '''
    Definisce un pezzo di profilo alluminio
    il punto di partenza è definito (0,0)
    '''

    def __init__(self, articolo: Articolo, lunghezza: int, punto_partenza: Vec2, direzione: Direzione, angolo_inizio: int = 90, angolo_fine: int = 90) -> None:

        self.articolo = articolo
        self.lunghezza = lunghezza
        self.punto_partenza = punto_partenza
        self.direzione = direzione
        self.angolo_inizio = angolo_inizio
        self.angolo_fine = angolo_fine

        self.coords = self.set_coords()


    def set_coords(self) -> Union[Vec2, Vec2, Vec2, Vec2]:
        '''
        Definisce i 4 punti in senso orario per disegnare la polyline del profilo
        Il profilo è considerato orizzontale, punto di partenza è in alto a SX
        '''
        larghezza = self.articolo.larghezza
        coords = [Vec2(0, 0), Vec2(self.lunghezza, 0)]
        if self.angolo_fine == 90:
            coords.append(Vec2(self.lunghezza, -larghezza))
        if self.angolo_fine == 45:
            coords.append(Vec2(self.lunghezza - larghezza, -larghezza))
        if self.angolo_inizio == 90:
            coords.append(Vec2(0, -larghezza))
        if self.angolo_inizio == 45:
            coords.append(Vec2(larghezza, -larghezza))
        return coords

    def min_x(self):
        return min(self.coords).x

    def max_x(self):
        return max(self.coords).x


class Struttura(ABC):
    '''Struttura perimetrale supporto pannello'''
    profili: Union[Profilo, Profilo, Profilo, Profilo] #4 profili per il giro anta
    quote: List[Quota]
    profilo_sx : Profilo
    profilo_su : Profilo
    profilo_dx : Profilo
    profilo_giu : Profilo

    def __init__(self, base: int, altezza: int) -> None:
        '''Base anta alluminio, Altezza anta alluminio'''
        self.base = base
        self.altezza = altezza
        self.profili = []
        self.quote = []

    def set_profili(self) -> None:
        self.profili = [self.profilo_sx, self.profilo_su, self.profilo_dx, self.profilo_giu]

    def set_quote(self) -> None:
        lpsx = self.profilo_sx.articolo.larghezza
        lpba = self.profilo_giu.articolo.larghezza
        self.quote.append(Quota(2, Vec2(lpsx, lpsx), Vec2(lpsx, self.altezza-lpsx), Lato.SX))
        self.quote.append(Quota(2, Vec2(lpba, lpba), Vec2(self.base-lpba, lpba), Lato.GIU))
        self.quote.append(Quota(3, Vec2(0, 0), Vec2(0, self.altezza), Lato.SX))
        self.quote.append(Quota(3, Vec2(0, 0), Vec2(self.base, 0), Lato.GIU))

class Struttura_normale(Struttura):
    '''Struttura perimetrale pannello a sormonto normale'''

    def __init__(self, base: int, altezza: int) -> None:
        super().__init__(base, altezza)
        
        self.base = base -8
        art = catalogo['AP31110']

        self.profilo_sx = Profilo(art, self.altezza, (0, 0), Direzione.SU, 45, 45)
        self.profilo_su = Profilo(art, self.base, (0, self.altezza), Direzione.DX, 45, 45)
        self.profilo_dx = Profilo(art, self.altezza, (self.base, self.altezza), Direzione.GIU, 45, 45)
        self.profilo_giu = Profilo(art, self.base, (self.base, 0), Direzione.SX, 45, 45)

        self.set_profili()
        self.set_quote()


if __name__ == '__main__':
    a = Articolo('myprofi', 50)
    p = Profilo(a,500,(0,0),Direzione.GIU)
    print(p.coords, p.min_x(), p.max_x())