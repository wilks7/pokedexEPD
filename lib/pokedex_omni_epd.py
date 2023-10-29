from omni_epd import displayfactory, EPDNotFoundError
import sys
from .pokedex.gen1_paper import Gen1
from .config import get_config
import random
from time import sleep

class PokedexEPD:
    def __init__(self, generation, version):
        try:
            epd = displayfactory.load_display_driver()
            resolution = (epd.width, epd.height)
            self.pokedex = Gen1(resolution, generation, version)

        except EPDNotFoundError:
            print(f"Couldn't find Display")
            sys.exit()

    def display(self, pokedex_entry, variant=None):
        epd = displayfactory.load_display_driver()
        epd.prepare()
        img = self.pokedex.draw_dex(pokedex_entry, variant)
        epd.display(img)
        epd.close


