from epdlib import Screen
from time import sleep
import logging
import random
from .pokeImage import getSprite
from .PokedexLayout import PokedexLayout
from .pokedex_api import get_pokemon_data
from .constants import POKEMON_RANGES

logging.root.setLevel('DEBUG')

class Pokedex:

    def __init__(self):
        self.screen = Screen(epd="HD", rotation=0, vcom=-1.58)
        width, height = self.screen.resolution
        self.layout = PokedexLayout(self.screen.resolution, 'L')
        self.width = width
        self.height = height

    def display(self, generation, pokedex):
        # Fetch Pokemon Data and Image
        pokemon = get_pokemon_data(pokedex)
        img = getSprite(generation, pokedex, self.height)
        
        # Update Layout contents
        self.layout.updatePokemon(pokemon, img)
        
        # Generate and write the layout to the EPD
        self.screen.writeEPD(self.layout.concat())

    def slideshow(self, generation, sorted=True, delay=5):
        start, end = POKEMON_RANGES.get(generation, (1, 151))
        pokedex_entries = list(range(start, end + 1))
        
        if not sorted:
            random.shuffle(pokedex_entries)

        for pokedex in pokedex_entries:
            self.display(generation, pokedex)
            sleep(delay)
