from lib.constants import GENERATIONS
from lib.pokedex.gen1_paper import Gen1
import random
from dataclasses import dataclass

class InvalidGenerationError(Exception):
    pass

@dataclass
class DisplayParameters:
    resolution: tuple
    generation: int
    version: str
    pokedex_entry: int
    variant: str

@dataclass
class Gen1Parameters(DisplayParameters):
    def __init__(self, resolution: tuple, pokedex_entry: int, version: str="red-blue", variant: str=None):
        super().__init__(resolution, generation=1, version=version, pokedex_entry=pokedex_entry, variant=variant)

def display_pokemon(resolution, pokedex, generation, version=None, variant=None):

    gen_data = _check_generation(generation)
    pokedex = _check_pokedex_entry(pokedex, gen_data)
    version = _check_version_for_generation(gen_data, version)
    variant = _check_variant(gen_data, variant)
    print(pokedex, generation, version)
    
    dex = Gen1(resolution, generation, version)
    img = dex.display(pokedex, variant)

    return img


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

def _check_variant(generation, variant):
    return None

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Display a Pokemon image.")

    parser.add_argument("--resolution", type=str, default="1872x1404")
    parser.add_argument("--generation", type=int, default=1)
    parser.add_argument("--version", type=str, default="red-blue")
    parser.add_argument("--pokemon", type=int, default=25)
    parser.add_argument("--variant", type=str, default=None)
    # You can add more arguments as needed.

    args = parser.parse_args()

    resolution = tuple(map(int, args.resolution.split('x')))
    generation = args.generation
    version = args.version
    pokemon = args.pokemon
    variant = args.variant

    img = display_pokemon(resolution, pokemon, generation, version, variant)
    img.show()
    # check_generation(range(152,252 ), generation, version, variant)

