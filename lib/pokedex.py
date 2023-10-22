from epdlib import Screen
from time import sleep
import logging
import random  # Import the random module

from .PokedexLayout import PokedexLayout
from .pokedex_api import get_pokemon_data

logging.root.setLevel('DEBUG')

def display(generation):
    # Create a Screen object and a PokedexLayout object
    my_screen = Screen(epd="HD", rotation=0, vcom=-1.58)
    my_layout = PokedexLayout(my_screen.resolution, 'L')

    # Get Pokémon data
    pokemon = get_pokemon_data(4)

    # Update the layout with Pokémon data
    my_layout.updatePokemon(pokemon)

    # Generate and write the layout to the EPD
    my_screen.writeEPD(my_layout.generate_layout())
