from epdlib import Screen
from lib.constants import POKEMON_RANGES
from lib.pokedex.pokedex_helper import Pokedex
from lib.pokedex.gen1_paper import Gen1
import random
from time import sleep
from lib.config import get_config

class PokedexPaper(Screen):
    def __init__(self, generation, version):
        epd = get_config("EPDLIB", "epd")
        vcom = float(get_config("IT8951.it8951", "vcom"))
        rotation = int(get_config("Display", "rotate"))
        super().__init__(epd=epd, rotation=rotation, vcom=vcom)
        self.pokedex = Gen1(self.resolution, generation, version)
        self.width, self.height = self.resolution

    def display(self, pokedex_entry, variant=None):
        img = self.pokedex.draw_dex(pokedex_entry, variant)

        self.writeEPD(img)

    def slideshow(self, sorted=None, delay=None, loop=None):
        sorted = sorted or bool(get_config("Slideshow", "sorted")) or True
        delay = delay or int(get_config("Slideshow", "delay")) or 10
        loop = loop or bool(get_config("Slideshow", "loop")) or False

        start, end = POKEMON_RANGES.get(self.pokedex.generation, None)
        pokedex_entries = list(range(start, end + 1))
        
        if not sorted:
            random.shuffle(pokedex_entries)

        for pokedex in pokedex_entries:
            self.display(pokedex)
            sleep(delay)


    
