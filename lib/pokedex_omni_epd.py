from omni_epd import displayfactory, EPDNotFoundError
import sys
from .pokedex.gen1_paper import Gen1
from .config import get_config
from .constants import POKEMON_RANGES
import random
from time import sleep

class PokedexEPD:
    def __init__(self, generation, version):
        try:
            resolution = (self.epd.width, self.epd.height)
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


    def slideshow(self, sorted=None, delay=None, loop=None):
        sorted = sorted or bool(get_config("Slideshow", "sorted")) or True
        delay = delay or get_config("Slideshow", "delay") or 10
        loop = loop or bool(get_config("Slideshow", "loop")) or False

        start, end = POKEMON_RANGES.get(self.pokedex.generation, None)
        pokedex_entries = list(range(start, end + 1))
        
        if not sorted:
            random.shuffle(pokedex_entries)

        for pokedex in pokedex_entries:
            self.display(pokedex)
            sleep(delay)

