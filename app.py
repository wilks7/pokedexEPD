import argparse
import configargparse
from lib import constants
from lib.pokedex.pokedex import PokedexPaper
import random
import os
import sys

def find_ini_file():
    # Get a list of files in the current directory
    files = os.listdir()

    # Look for any .ini files in the current directory
    for file in files:
        if file.endswith(".ini"):
            return file

    # If no .ini file is found, return None
    return None


def _check_generation(pokedex, generation):
    if generation is None:
        for gen, (start, end) in constants.POKEMON_RANGES.items():
            if pokedex <= end:
                return gen
    else:
        if 0 < generation < 10:
            (start,end) = constants.POKEMON_RANGES[generation]
            if pokedex > end:
                print("Invalid Generation")
                sys.exit(1)  # Exit with an error code
            return generation
        else:
            print("Invalid Generation")
            sys.exit(1)  # Exit with an error code



def main():
    # Find the first .ini file in the current directory
    config_file = find_ini_file()

    # Create a parser that allows reading arguments from both command-line and config file
    parser = configargparse.ArgParser(
        default_config_files=[config_file] if config_file else [],
        description="Display Pokedex entries from a specific generation on an e-paper display."
    )
    parser.add_argument('--config', is_config_file=True, help='Config file path')

    parser.add_argument('--epd', type=str, required=True, help="The Waveshare EPD type")
    parser.add_argument('--rotation', type=int, default=0, help="The rotation of the display")
    parser.add_argument('--vcom', type=float, default=-1.58, help="The VCOM value as a negative number")

    parser.add_argument('--generation','-gen', type=int, default=None, help="Name of the Pokemon generation to display (e.g., 'Gen1', 'Gen2', etc.).")
    parser.add_argument('--pokedex', '-p', type=int, default=None, help="Number of the Pokemon's Pokedex entry (e.g., 1, 2, etc.).")
    
    parser.add_argument('--slideshow', action='store_true', help="Start a slideshow to display the Pokemon entries")
    parser.add_argument('--sorted', action='store_true', help="Order to display the Pokemon entries")
    parser.add_argument('--delay', type=int, default=60, help="Delay between slideshow items")

    args = parser.parse_args()


    print("Initializing Display")

    if args.slideshow:
        if args.generation is None:
            args.generation = random.randint(1,9)
        print(f"Starting Gen {args.generation} Slideshow with {args.delay} seconds, sorted: {args.sorted}")

        pokedex = PokedexPaper(args.epd, args.rotation, args.vcom, args.generation)
        pokedex.slideshow(args.generation, args.sorted, args.delay)
    else:
        if args.pokedex is None and args.generation is None:
            args.generation = random.randint(1,9)
            start, end = constants.POKEMON_RANGES[args.generation]
            args.pokedex = random.randint(start, end)

        args.generation = _check_generation(args.pokedex, args.generation)

        pokedex = PokedexPaper(args.epd, args.rotation, args.vcom, args.generation)
        pokedex.display(args.pokedex, args.generation)

if __name__ == "__main__":
    main()
