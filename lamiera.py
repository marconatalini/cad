from abc import ABC
from dataclasses import dataclass
from typing import List, Union
from dim import Quota, Lato
from profilo import Direzione

from ezdxf.math import Vec2

class Incisione():
    '''
    Orizzontali partono da SX
    Verticali partono dal GIU
    '''
    coords: Union[Vec2, Vec2, Vec2, Vec2]
    
    def __init__(self, lunghezza: int, punto_partenza: Vec2, direzione: Direzione, thick: int = 8) -> None:
        
        self.lunghezza = lunghezza
        self.punto_partenza = punto_partenza
        self.direzione = direzione
        self.thick = thick
        self.set_coords()

    def set_coords(self) -> None:
        '''Punto di partenza = inizio dell'asse dell'incisione ''' 
        self.coords = [Vec2(0, self.thick/2),Vec2(self.lunghezza, self.thick/2),Vec2(self.lunghezza, -self.thick/2),Vec2(0, -self.thick/2)]



class Lamiera(ABC):
    '''Definizione generica di Lamiera per pannello'''
    incisioni : List[Incisione]
    coords : Union[Vec2, Vec2, Vec2, Vec2]
    quote : List[Quota]

    def __init__(self, base: int, altezza: int, piega: int = 0) -> None:
        self.base_lamiera = base
        self.altezza_lamiera = altezza
        self.piega = piega
        self.incisioni = []
        self.coords = []
        self.quote = []
        self.set_coords()

    def set_coords(self) -> None:
        self.coords = [Vec2(-self.piega,0), Vec2(-self.piega, self.altezza_lamiera), 
            Vec2(self.base_lamiera -self.piega, self.altezza_lamiera), Vec2(self.base_lamiera -self.piega, 0) ]

    def add_incisione(self, incisione: Incisione) -> None:
        self.incisioni.append(incisione)
        
class Lamiera_sormonto(Lamiera):
    '''definizione Lamiera'''

    def __init__(self, base: int, altezza: int, piega: int) -> None:
        super().__init__(base, altezza, piega)
        self.base_lamiera = base -8 + (2* self.piega)
        self.set_quote()
        self.set_coords()
    
    def set_quote(self) -> None:
        self.quote.append(Quota(1, Vec2(-self.piega, 0), Vec2(-self.piega, self.altezza_lamiera), Lato.SX))
        self.quote.append(Quota(1, Vec2(-self.piega, 0), Vec2(self.base_lamiera-self.piega, 0), Lato.GIU))        

    def set_quote_incisioni(self) -> None:
        y_quote_incisioni = [0]
        for incisione in self.incisioni:
            y_quote_incisioni.append(incisione.punto_partenza.y)
        y_quote_incisioni.append(self.altezza_lamiera)

        for i, y in enumerate(y_quote_incisioni[:-1]):
            x = self.base_lamiera
            self.quote.append(Quota(1,
                Vec2(x, y_quote_incisioni[i]),
                Vec2(x, y_quote_incisioni[i+1]),
                Lato.DX ))

if __name__ == '__main__':
    l = Lamiera_sormonto(800,2200,20)