from epdlib import Screen
from time import sleep
import logging
import random
from .pokeImage import getSprite
from .PokedexLayout import PokedexLayout
from .pokedex_api import get_pokemon_data
from .constants import POKEMON_RANGES

logging.root.setLevel('DEBUG')


def display(generation, pokedex):
    # Create a Screen object and a PokedexLayout object
    my_screen = Screen(epd="HD", rotation=0, vcom=-1.58)
    widht,height = my_screen.resolution
    my_layout = PokedexLayout(my_screen.resolution, 'L')

    # Fetch Pokemon Data and Image
    pokemon = get_pokemon_data(pokedex)
    img = getSprite(generation, pokedex, height)

    # Update Layout contents
    my_layout.updatePokemon(pokemon, img)

    # Generate and write the layout to the EPD
    my_screen.writeEPD(my_layout.concat())


def slideshow(generation, sorted=True, delay=5):
    start, end = POKEMON_RANGES.get(generation, (1, 151))
    
    # Create a list of Pokedex numbers in the specified range.
    pokedex_entries = list(range(start, end + 1))
    
    # If not sorted, shuffle the list to randomize the order.
    if not sorted:
        random.shuffle(pokedex_entries)
    
    # Loop through each Pokedex number and display the Pokémon.
    for pokedex in pokedex_entries:
        display(generation, pokedex)
        sleep(delay)

