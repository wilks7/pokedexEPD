from epdlib import Screen
from time import sleep
import logging
import random

from .pokeImage import fetchSprite
from .PokedexLayout import PokedexLayout
from .pokedex_api import build_pokemon
from .constants import POKEMON_RANGES

# logging.root.setLevel('DEBUG')

class PokedexPaper:
    def __init__(self, epd, rotation, vcom):
        self.screen = Screen(epd=epd, rotation=rotation, vcom=vcom)
        print("Resolution", self.screen.resolution)
        width, height = self.screen.resolution
        self.layout = PokedexLayout(self.screen.resolution, 'L')
        self.width = width
        self.height = height

    def display(self, generation, pokedex):
        pokemon = build_pokemon(pokedex, generation)
        img = fetchSprite(pokemon.sprite, self.height)
        
        print("Displaying: ", pokemon.species)
        self.layout.updatePokemon(pokemon, img)
        
        self.screen.writeEPD(self.layout.concat())

    def slideshow(self, generation, sorted=True, delay=10):
        start, end = POKEMON_RANGES.get(generation, (1, 151))
        pokedex_entries = list(range(start, end + 1))
        
        if not sorted:
            random.shuffle(pokedex_entries)

        for pokedex in pokedex_entries:
            self.display(generation, pokedex)
            sleep(delay)
        # self.screen.clearEPD()
