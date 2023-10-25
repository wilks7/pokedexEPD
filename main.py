import configargparse
from lib import constants
from pokedex_epd import PokedexEPD
import random
import os
import sys


def main():
    config_file = os.path.join(os.getcwd(), 'config.ini')
    
    parser = configargparse.ArgParser(
        default_config_files=[config_file] if config_file else [],
        description="Display Pokedex entries from a specific generation on an e-paper display."
    )


    parser.add_argument('--pokedex', '-p', type=int, default=None, help="Number of the Pokemon's Pokedex entry (e.g., 1, 2, etc.).")
    parser.add_argument('--generation','-gen', type=int, required=True, help="Name of the Pokemon generation to display (e.g., 'Gen1', 'Gen2', etc.).")
    parser.add_argument('--version', type=str, default=None, help="Version game of the generation.")

    parser.add_argument('--slideshow', action='store_true', help="Start a slideshow to display the Pokemon entries")

    parser.add_argument('--config', is_config_file=True, help='Config file path')

    args = parser.parse_known_args()


    generation = args.generation
    
    pokedexEPD = PokedexEPD(generation, args.version)

    if args.slideshow:
        pokedexEPD.slideshow()
    else:
        pokedex = args.pokedex
        if pokedex is None :
            pokedex = random.randint(constants.POKEMON_RANGES[generation])
            
        _check_generation(pokedex, generation)
        pokedexEPD.display(args.pokedex, args.generation)

def _check_generation(pokedex, generation):
    if 0 < generation < 10:
        (start,end) = constants.POKEMON_RANGES[generation]
        if pokedex > end:
            print("Invalid Generation")
            sys.exit(1)  # Exit with an error code
    else:
        print("Invalid Generation")
        sys.exit(1)  # Exit with an error code

if __name__ == "__main__":
    main()
