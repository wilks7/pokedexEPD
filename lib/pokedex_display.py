from lib.constants import POKEMON_RANGES
from lib.pokedex_omni_epd import PokedexEPD
from time import sleep
import random
from lib.config import get_config

class InvalidGenerationError(Exception):
    pass

def display_pokemon(pokedex, generation, version=None):
    _check_generation(pokedex, generation)
    
    pokedexEPD = PokedexEPD(generation, version)
    pokedexEPD.display(pokedex)

def start_slideshow(generation, version=None):
    sorted_entries = bool(get_config("Slideshow", "sorted")) or True
    delay = int(get_config("Slideshow", "delay")) or 10

    start, end = POKEMON_RANGES.get(generation, None)
    pokedex_entries = list(range(start, end + 1))
    
    if not sorted_entries:
        random.shuffle(pokedex_entries)

    for pokedex in pokedex_entries:
        display_pokemon(pokedex, generation, version)
        sleep(delay)

def _check_generation(pokedex, generation):
    if 0 < generation < 10:
        (start, end) = POKEMON_RANGES[generation]
        if pokedex > end:
            raise InvalidGenerationError(f"Pokedex number {pokedex} does not belong to Generation {generation}.")
    else:
        raise InvalidGenerationError(f"Invalid Generation {generation}.")
