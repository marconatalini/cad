from abc import ABC
from dataclasses import dataclass
from dim import Quota, Lato
from profilo import Direzione

from ezdxf.math import Vec2

@dataclass
class Incisione():
    '''
    Orizzontali partono da SX ed hanno direzione ORIzzontale
    Verticali partono dal GIU ed hanno direzione VERticale
    '''

    lunghezza: int
    punto_partenza: tuple
    direzione: Direzione
    thick: int = 8

    def coords(self):
        '''Punto di partenza = inizio dell'asse dell'incisione ''' 
        return[(0, self.thick/2),(self.lunghezza, self.thick/2),(self.lunghezza, -self.thick/2),(0, -self.thick/2)]

    def get_y(self):
        return self.punto_partenza[1]

    def get_x(self):
        return self.punto_partenza[0]

class Lamiera(ABC):
    '''Definizione Lamiera pannello'''
    
    def __init__(self, base: int, altezza: int, piega: int = 0):
        '''creo lamiera partendo dalle misure anta alluminio'''
        self.base_lamiera = base
        self.altezza_lamiera = altezza
        self.piega = piega
        self.incisioni = []
    
    def add_incisione(self, incisione: Incisione):
        self.incisioni.append(incisione)
        
class Lamiera_sormonto(Lamiera):
    '''definizione Lamiera'''

    def __init__(self, base: int, altezza: int, piega: int):
        super().__init__(base, altezza, piega)
        self.base_lamiera = base -8 +(2* self.piega)

    def coords(self):
        return[(-self.piega,0,0), (-self.piega, self.altezza_lamiera,0), 
            (self.base_lamiera - self.piega, self.altezza_lamiera,0), (self.base_lamiera - self.piega, 0,0) ]

    def quote(self):
        result = []
        result.append(Quota(1, Vec2(-self.piega, 0), Vec2(-self.piega, self.altezza_lamiera), Lato.SX))
        result.append(Quota(1, Vec2(-self.piega, 0), Vec2(self.base_lamiera-self.piega, 0), Lato.GIU))        

        y_quote_incisioni = [0]
        for incisione in self.incisioni:
            y_quote_incisioni.append(incisione.get_y())
        y_quote_incisioni.append(self.altezza_lamiera)

        for i, y in enumerate(y_quote_incisioni[:-1]):
            x = self.base_lamiera
            result.append(Quota(1,
                Vec2(x, y_quote_incisioni[i]),
                Vec2(x, y_quote_incisioni[i+1]),
                Lato.DX ))
            
        return result

if __name__ == '__main__':
    pass