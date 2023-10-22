from epdlib import Screen
from time import sleep
import logging
import random  # Import the random module

from PokedexLayout import PokedexLayout
from pokedex_api import get_pokemon_data

logging.root.setLevel('DEBUG')

# Create a Screen object and a PokedexLayout object
my_screen = Screen(epd="HD", rotation=0, vcom=-1.58)
my_layout = PokedexLayout(my_screen.resolution, 'L')

# Loop through Pokémon numbers 1 to 151
for number in range(1, 152):
    # Get Pokémon data
    pokemon = get_pokemon_data(number)
    
    # Update the layout with Pokémon data
    my_layout.updatePokemon(pokemon)

    # Generate and write the layout to the EPD
    my_screen.writeEPD(my_layout.generate_layout())
    
    # Sleep for 10 seconds before clearing the screen
    sleep(10)
    
    # Clear the screen
    # my_screen.clearEPD()

# while True:
#     # Generate a random number between 1 and 151 (inclusive)
#     random_number = random.randint(1, 151)
    
#     # Get Pokémon data for the random number
#     pokemon = get_pokemon_data(random_number)
    
#     # Update the layout with Pokémon data
#     my_layout.updatePokemon(pokemon)

#     # Generate and write the layout to the EPD
#     my_screen.writeEPD(my_layout.generate_layout())
    
#     # Sleep for 10 seconds before clearing the screen
#     sleep(360)
    
#     # Clear the screen
#     my_screen.clearEPD()