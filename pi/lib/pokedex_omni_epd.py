from omni_epd import displayfactory, EPDNotFoundError
import sys
from .pokedex.gen1_paper import Gen1
from .config import get_config
import random
from time import sleep

class PokedexEPD:
    def __init__(self, generation, version):
        try:
            self.epd = displayfactory.load_display_driver()
            self.resolution = (self.epd.width, self.epd.height)
            self.generation = generation
            self.version = version

        except EPDNotFoundError:
            print(f"Couldn't find Display")
            sys.exit()

    def display(self, pokedex_entry, variant=None):
        pokedex = Gen1(self.resolution, self.generation, self.version)
        # epd = displayfactory.load_display_driver()
        self.epd.prepare()
        img = pokedex.draw_dex(pokedex_entry, variant)
        self.epd.display(img)
        self.epd.close


