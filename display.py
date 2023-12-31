from lib.constants import GENERATIONS
from lib.pokedex_omni_epd import PokedexEPD
from time import sleep
import random
from lib.config import get_config

class InvalidGenerationError(Exception):
    pass

def display_pokemon(pokedex, generation, version=None):

    gen_data = _check_generation(generation)
    pokedex = _check_pokedex_entry(pokedex, gen_data)

    version = _check_version_for_generation(gen_data, version)
    print(pokedex, generation, version)
    
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



def _check_generation(generation):
    gen_data = GENERATIONS.get(generation, None)
    if gen_data:
        return gen_data
    else:
        raise InvalidGenerationError(f"Invalid Generation {generation}.")
    

def _check_pokedex_entry(pokedex, gen_data):
    start, end = gen_data['range']

    if pokedex is None:
        return random.randint(*gen_data['range'])

    if not (1 <= pokedex <= end):
        raise InvalidGenerationError(f"Pokedex number {pokedex} does not belong to Generation {gen_data['title']}.")
    else:
        return pokedex


def _check_version_for_generation(gen_data, version=None):

    # If no version is provided, return the first version for the given generation
    if version is None:
        return list(gen_data['versions'].keys())[0]

    # Check if the provided version is valid for the given generation
    if version not in gen_data['versions']:
        raise InvalidGenerationError(f"Version {version} is not valid for Generation {gen_data['title']}.")

    return version


