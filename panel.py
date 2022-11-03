from abc import ABC, abstractmethod
from curses.ascii import alt
from enum import Enum, auto

from lamiera import Lamiera, Incisione, Lamiera_sormonto
from profilo import Articolo, Direzione, Profilo, Struttura, Struttura_1
from dim import Quota, Lato

class Apertura(Enum):
    TIRARE_DESTRA = auto()
    TIRARE_SINISTRA = auto()

class Panel(ABC):

    def __init__(self, base: int, altezza: int, apertura: Apertura = Apertura.TIRARE_DESTRA) -> None:
        '''Pannello creto sulla misura dell'anta di alluminio'''
        self.base = base -8
        self.altezza = altezza
        self.apertura = apertura
        self.struttura = Struttura(base, altezza)
        self.supporti = []
        self.lamiera = Lamiera(base, altezza)


class Ametista4(Panel):
    '''Definizione del modello Ametista'''

    NUMERO_INCISIONI = 4

    def __init__(self, base: int, altezza: int, apertura: Apertura = Apertura.TIRARE_DESTRA) -> None:
        super().__init__(base, altezza, apertura)
        
        self.struttura = Struttura_1(base, altezza)
        self.lamiera = Lamiera_sormonto(base, altezza, 17)
        
        self.set_supporti()
        self.set_incisioni()

    def set_supporti(self) -> list:
        art = Articolo('AP31.110', 31)    
        self.supporti.append(Profilo(art, self.altezza - art.larghezza*2, (144, art.larghezza,0), Direzione.SU))
        self.supporti.append(Profilo(art, self.altezza - art.larghezza*2, (self.base - 144, self.altezza - art.larghezza,0), Direzione.GIU))
        if self.base - (144*2) > 400:
            self.supporti.append(Profilo(art, self.altezza - art.larghezza*2, (415, art.larghezza,0), Direzione.SU))

    def quote_supporti(self) -> list:
        result = []
        p_largh = self.struttura.profili[0].articolo.larghezza
        x_quote = [0+p_largh,self.base-p_largh]

        for supporto in self.supporti:
            x_quote.append(supporto.punto_partenza[0])
            x_quote.append(supporto.punto_partenza[0]+supporto.articolo.larghezza)
        
        sort_x = sorted(x_quote)
        print(sort_x)
        for i, value in enumerate(sort_x[:-1]):
            q = Quota(1, (sort_x[i], 0), (sort_x[i+1], 0), Lato.GIU)
            if q.lunghezza_quota() > p_largh:
                result.append(q)
        print(result)
        return result

    def set_incisioni(self) -> list:
        # da_sotto = int(input(f"Misura prima incisione da sotto lamiera? "))
        # da_sopra = int(input(f"Misura ultima incisione da sopra lamiera? "))
        da_sotto = 250
        da_sopra = 200
        for i in range(self.NUMERO_INCISIONI):
            y = da_sotto + i *((self.altezza-da_sopra-da_sotto) / (self.NUMERO_INCISIONI-1))
            self.lamiera.add_incisione(Incisione(self.base, (0,int(y),0), Direzione.ORIZZONTALE))
        

if __name__ == '__main__':
    pass