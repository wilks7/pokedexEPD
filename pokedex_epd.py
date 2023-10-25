from epdlib import Screen
from lib.layout.PokedexLayout import PokedexLayout
from lib.constants import POKEMON_RANGES
from pokedex import PokedexHelper
import random
from time import sleep
from config import get_config

class PokedexEPD(Screen, PokedexHelper):
    def __init__(self, generation, version):
        epd = get_config("Display", "epd")
        vcom = get_config("Display", "vcom")
        rotation = get_config("Display", "rotation")

        super().__init__(epd=epd, rotation=rotation, vcom=vcom)
        PokedexHelper.__init__(self, generation, version)

        self.width, self.height = self.resolution

    def display(self, pokedex, variant=None):
        pokemon = self.get_pokemon(pokedex)
        sprite = self.get_image(pokedex, variant, self.height)

        layout = PokedexLayout(self.resolution, 'L', self.generation)
        layout.updatePokemon(pokemon, sprite)

        img = layout.concat()

        self.writeEPD(img)

    def slideshow(self, sorted=None, delay=None, loop=None):
        sorted = sorted or get_config("Slideshow", "sorted") or True
        delay = delay or get_config("Slideshow", "delay") or 10
        loop = loop or get_config("Slideshow", "loop") or False

        start, end = POKEMON_RANGES.get(self.generation, None)
        pokedex_entries = list(range(start, end + 1))
        
        if not sorted:
            random.shuffle(pokedex_entries)

        for pokedex in pokedex_entries:
            self.display(pokedex)
            sleep(delay)


    
