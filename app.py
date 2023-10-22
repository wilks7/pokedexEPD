import argparse
from lib import constants
from lib.pokedex import PokedexPaper
import random


def main():
    parser = argparse.ArgumentParser(description="Display Pokedex entries from a specific generation on an e-paper display.")
    parser.add_argument('--generation', type=str, default='', help="Name of the Pokemon generation to display (e.g., 'Gen1', 'Gen2', etc.).")
    parser.add_argument('--pokedex', type=int, default=0, help="Number of the Pokemon's Pokedex entry (e.g., 1, 2, etc.).")
    parser.add_argument('--slideshow', action='store_false', help="Start a slideshow to display the Pokemon entries")
    parser.add_argument('--sorted', action='store_true', help="Order to display the Pokemon entries")

    args = parser.parse_args()
    generation = args.generation
    pokedex_entry = args.pokedex

    game = ''
    if game == '':
        game = constants.DEFAULT_GAMES.get(generation, "")
    if pokedex_entry == 0:
        start, end = constants.POKEMON_RANGES.get(generation, (1, 151))
        pokedex_entry = random.randint(start, end)

    pokedex = PokedexPaper()
    print(args)

    if args.slideshow:
        pokedex.slideshow(generation, args.sorted)
    else:
        pokedex.display(generation, pokedex_entry)




if __name__ == "__main__":
    main()
