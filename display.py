from lib.constants import GENERATIONS
from lib.pokedex_omni_epd import PokedexEPD
from time import sleep
import random
from lib.config import get_config

class InvalidGenerationError(Exception):
    pass

def display_pokemon(pokedex, generation, version=None):

                
    generation = _check_generation(generation)
    pokedex = _check_pokedex_entry(pokedex, generation)

    version = _check_version_for_generation(generation, version)
    
    pokedexEPD = PokedexEPD(generation, version)
    pokedexEPD.display(pokedex)

def start_slideshow(generation, version=None):
    sorted_entries = bool(get_config("Slideshow", "sorted")) or True
    delay = int(get_config("Slideshow", "delay")) or 10

    gen_data = GENERATIONS.get(generation, None)
    if not gen_data:
        raise InvalidGenerationError(f"Invalid Generation {generation}.")
        
    start, end = gen_data['range']
    pokedex_entries = list(range(start, end + 1))
    
    if not sorted_entries:
        random.shuffle(pokedex_entries)

    for pokedex in pokedex_entries:
        display_pokemon(pokedex, generation, version)
        sleep(delay)


def _check_pokedex_entry(pokedex, gen_data):
    start, end = gen_data['range']

    if not pokedex:
        return random.randint(*gen_data['range'])

    if not (start <= pokedex <= end):
        raise InvalidGenerationError(f"Pokedex number {pokedex} does not belong to Generation {gen_data['title']}.")


def _check_generation(generation):
    gen_data = GENERATIONS.get(generation, None)
    if gen_data:
        return generation
    else:
        raise InvalidGenerationError(f"Invalid Generation {generation}.")

def _check_version_for_generation(generation, version=None):
    gen_data = GENERATIONS.get(generation, None)
    if not gen_data:
        raise InvalidGenerationError(f"Invalid Generation {generation}.")

    if version is None:
        return gen_data['versions'][0]

    if version not in gen_data['versions']:
        raise InvalidGenerationError(f"Version {version} is not valid for Generation {generation}.")

    return version

