from cgi import print_arguments
import math
import ezdxf
from ezdxf.math import UCS, intersection_line_line_3d, Vec2
from ezdxf import units, zoom
from ezdxf.tools.standards import setup_dimstyle
from ezdxf.render.arrows import ARROWS
from dim import Quota

from panel import Ametista4, Panel

from profilo import Direzione, Profilo
from lamiera import Incisione, Lamiera

OFFSET_DIM_BASE = 100

def set_offset_quota(dim: Quota):
    dim.offset = dim.row * OFFSET_DIM_BASE
    return dim

class Cad():

    layers_dict = {
        "Alluminio_ante_1": 6,
        "Lamiera-Coprifili": 1,
        "Quote_Alu_Lamiera": 3,
        "Quote_Alu_Lamiera_1": 3,
        "Quote_AluAnta_1": 3,
    }

    def __init__(self, panel: Panel) -> None:
        self.nome_disegno = f"{panel.__class__.__name__}_{panel.base}x{panel.altezza}"
        self.doc = ezdxf.new(setup=True)
        self.doc.units = units.MM
        setup_dimstyle(self.doc, "EZ_MM_1_H25_MM")
        my_dimstyle = setup_dimstyle(
                            self.doc,
                            name="MARCO",
                            fmt="EZ_MM_1_H25_MM",
                            # style=options.default_dimension_text_style,
                            blk=ARROWS.closed_filled,
                        )
        my_dimstyle.dxf.dimscale = 10  
        self.doc.header["$DIMSTYLE"] = "MARCO"
        my_dimstyle.copy_to_header(self.doc)

        self.msp = self.doc.modelspace()
        self.panel = panel

        for key, value in self.layers_dict.items():
            self.doc.layers.add(name=key, color=value)

        
    def draw_profilo(self, profilo: Profilo, with_text = False):
        ucs = self._ucs(profilo.punto_partenza, profilo.direzione)
        ocs_point = list(ucs.points_to_ocs(profilo.coords()))
        self.msp.add_lwpolyline(ocs_point, close=True, dxfattribs={"layer" : "Alluminio_ante_1"})
        if with_text:
            # Using a text style
            center = intersection_line_line_3d((ocs_point[0],ocs_point[2]),(ocs_point[1],ocs_point[3]))
        
            self.msp.add_text(profilo.articolo.codice, rotation=profilo.direzione.value, 
                height=profilo.articolo.larghezza * .8,
                dxfattribs={'layer': 'Quote_AluAnta_1',}
                ).set_pos(center, align='MIDDLE_CENTER')

    def draw_lamiera(self, lamiera: Lamiera):
        self.msp.add_lwpolyline(lamiera.coords(), close=True, dxfattribs={"layer" : "Lamiera-Coprifili"})

    def draw_incisione(self, incisione: Incisione):
        ucs = self._ucs(incisione.punto_partenza, incisione.direzione)
        ocs_point = list(ucs.points_to_ocs(incisione.coords()))
        self.msp.add_lwpolyline(ocs_point, close=True, dxfattribs={"layer" : "Lamiera-Coprifili"})
    
    def quotatura(self, lista_quote: list, layer: str = 'Quote'):
        quote = map(set_offset_quota, lista_quote)
        for q in list(quote):
            dim = self.msp.add_linear_dim(
                base=q.get_punto_base(),  # location of the dimension line
                p1=q.p1,  # 1st measurement point
                p2=q.p2,  # 2nd measurement point
                angle=q.get_angle(), # angle dimension
                dimstyle="MARCO",  # default dimension style
                dxfattribs={'layer': layer,}
            ).render()


    def _ucs(self, origin: tuple, direzione: Direzione) -> UCS:
        ucs = UCS(origin)
        if direzione == Direzione.SU or direzione == Direzione.VERTICALE: 
            ucs = ucs.rotate_local_z(math.radians(Direzione.SU.value))
        if direzione == Direzione.GIU: 
            ucs = ucs.rotate_local_z(math.radians(Direzione.GIU.value))
        if direzione == Direzione.SX: 
            ucs = ucs.rotate_local_z(math.radians(Direzione.SX.value))
        return ucs

    def save(self):
        '''Disegna pannello e salva il file'''
        
        for profilo in self.panel.struttura.profili:
            self.draw_profilo(profilo, True)

        for profilo in self.panel.supporti:
            self.draw_profilo(profilo, True)

        self.draw_lamiera(self.panel.lamiera)
        self.quotatura(self.panel.lamiera.quote(), 'Quote_Alu_Lamiera')

        for incisione in self.panel.lamiera.incisioni:
            self.draw_incisione(incisione)


        zoom.extents(self.msp)
        self.doc.saveas(f"{self.nome_disegno}.dxf")

if __name__ == '__main__':
    p = Ametista4(985,2130)
    d = Cad(p)
    d.save()