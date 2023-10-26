import configargparse
from lib.constants import POKEMON_RANGES
from lib.pokedex_epdlib import PokedexPaper
from lib.pokedex import gen1_paper
import random
import os
import sys
from time import sleep
from .lib.config import get_config

def main():
    config_file = os.path.join(os.getcwd(), 'omni-epd.ini')
    
    parser = configargparse.ArgParser(
        default_config_files=[config_file] if config_file else [],
        description="Display Pokedex entries from a specific generation on an e-paper display."
    )


    parser.add_argument('--pokedex', '-p', type=int, default=None, help="Number of the Pokemon's Pokedex entry (e.g., 1, 2, etc.).")
    parser.add_argument('--generation','-gen', type=int, required=True, help="Name of the Pokemon generation to display (e.g., 'Gen1', 'Gen2', etc.).")
    parser.add_argument('--version', type=str, default=None, help="Version game of the generation.")

    parser.add_argument('--slideshow', action='store_true', help="Start a slideshow to display the Pokemon entries")

    parser.add_argument('--config', is_config_file=True, help='Config file path')

    args, _ = parser.parse_known_args()
    
    # pokedexEPD = PokedexPaper(args.generation, args.version)
    if args.slideshow:
        from lib.pokedex_epdlib import PokedexPaper
        sorted = bool(get_config("Slideshow", "sorted")) or True
        delay = int(get_config("Slideshow", "delay")) or 10
        loop = bool(get_config("Slideshow", "loop")) or False

        start, end = POKEMON_RANGES.get(args.generation, None)
        pokedex_entries = list(range(start, end + 1))
        
        if not sorted:
            random.shuffle(pokedex_entries)

        for pokedex in pokedex_entries:
            pokedexPaper = PokedexPaper(args.generation, args.version)
            pokedexPaper.display(pokedex)
            sleep(delay)

    else:
        from lib.pokedex_omni_epd import PokedexEPD

        pokedexEPD = PokedexEPD(args.generation, args.version)
        pokedex = args.pokedex
        if pokedex is None :
            pokedex = random.randint(POKEMON_RANGES[args.generation])
            
        _check_generation(pokedex, args.generation)
        pokedexEPD.display(args.pokedex, None)

def _check_generation(pokedex, generation):
    if 0 < generation < 10:
        (start,end) = POKEMON_RANGES[generation]
        if pokedex > end:
            print("Invalid Generation")
            sys.exit(1)  # Exit with an error code
    else:
        print("Invalid Generation")
        sys.exit(1)  # Exit with an error code




if __name__ == "__main__":
    main()
