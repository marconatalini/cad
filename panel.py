from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import List

from ezdxf.math import Vec2

from lamiera import Lamiera, Incisione, Lamiera_sormonto
from profilo import Articolo, Direzione, Profilo, Struttura, Struttura_normale
from dim import Quota, Lato

class Apertura(Enum):
    TIRARE_DESTRA = auto()
    TIRARE_SINISTRA = auto()


class Panel(ABC):
    base : int
    altezza : int
    apertura : Apertura = Apertura.TIRARE_DESTRA
    numero_incisioni : int
    struttura : Struttura
    lamiera : Lamiera
    supporti : List[Profilo]

    @abstractmethod
    def __init__(self) -> None:
        '''Pannello creto sulla misura dell'anta di alluminio'''

    @abstractmethod
    def set_supporti(self) -> None:
        '''definisce i supporti necessari per questo pannello'''

    @abstractmethod
    def set_incisioni(self) -> None:
        '''aggiunge le incisioni alla lamiera di questo pannello'''


class Ametista_a_sormonto(Panel):
    '''Definizione del modello Ametista generico'''

    def __init__(self, base: int, altezza: int, numero_incisioni: int) -> None:
        self.base = base -8
        self.altezza = altezza
        self.numero_incisioni = numero_incisioni
        self.struttura = Struttura_normale(base, altezza)
        self.lamiera = Lamiera_sormonto(base, altezza, 17)
        self.supporti = []
        
        self.set_supporti()
        self.set_incisioni()

    def set_supporti(self) -> None:
        art = Articolo('AP31.110', 31)    
        self.supporti.append(Profilo(art, self.altezza - art.larghezza*2, (144, art.larghezza,0), Direzione.SU))
        self.supporti.append(Profilo(art, self.altezza - art.larghezza*2, (self.base - 144, self.altezza - art.larghezza,0), Direzione.GIU))
        if self.base - (144*2) > 400:
            self.supporti.append(Profilo(art, self.altezza - art.larghezza*2, (415, art.larghezza,0), Direzione.SU))

    def set_incisioni(self) -> list:
        if self.numero_incisioni > 3:
            da_sotto = input_numero(f"Misura prima incisione da SOTTO lamiera? INVIO = equidistanti : ")
            da_sopra = input_numero(f"Misura ultima incisione da SOPRA lamiera? INVIO = equidistanti : ")
            interasse = (self.altezza - da_sopra - da_sotto) / (self.numero_incisioni + 1  - 1 * bool(da_sotto) - 1 * bool(da_sopra))
        for i in range(self.numero_incisioni):
            y = da_sotto + i * interasse
            if y: self.lamiera.add_incisione(Incisione(self.base, Vec2(0, y), Direzione.ORIZZONTALE))
        self.lamiera.set_quote_incisioni()

class Ametista_32_a_sormonto(Ametista_a_sormonto):
    '''Modello Ametista 3.2'''

    def __init__(self, base: int, altezza: int, numero_incisioni: int = 6) -> None:
        super().__init__(base, altezza, numero_incisioni)

    def set_supporti(self) -> None:
        return super().set_supporti()
        
    def set_incisioni(self) -> list:
        n_gruppi_incisioni = int(self.numero_incisioni/2)
        interasse = (self.altezza - n_gruppi_incisioni * 100) / (n_gruppi_incisioni + 1)
        for i in range(n_gruppi_incisioni + 1): # 3 gruppi di incisioni doppie
            y = i * (interasse + 100)
            if y: 
                self.lamiera.add_incisione(Incisione(self.base, Vec2(0, y-100), Direzione.ORIZZONTALE))
                self.lamiera.add_incisione(Incisione(self.base, Vec2(0, y), Direzione.ORIZZONTALE))
        self.lamiera.set_quote_incisioni()

class Ametista_42_a_sormonto(Ametista_32_a_sormonto):
    '''Modello Ametista 4.2'''

    def __init__(self, base: int, altezza: int, numero_incisioni: int = 8) -> None:
        super().__init__(base, altezza, numero_incisioni)

    def set_supporti(self) -> None:
        return super().set_supporti()

    def set_incisioni(self) -> list:
        return super().set_incisioni()

def input_numero(domanda: str) -> int:
    while True:
        n = input(domanda)
        if not n: return 0
        if n.isnumeric(): return int(n)
        print("Inserire un numero! Riprova. ")

if __name__ == '__main__':
    p = Ametista_32_a_sormonto(800,2200,4)