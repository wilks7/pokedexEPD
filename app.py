import argparse
from lib import pokedex
import random


DEFAULT_GAMES = {
    "Gen1": "red-blue",
    "Gen2": "silver",
    "Gen3": "ruby-sapphire"
    # Add more defaults for other generations if needed
}

POKEMON_RANGES = {
    "Gen1": (1, 151),
    "Gen2": (1, 251),
    "Gen3": (1, 386),
    # Add ranges for other generations if needed
}

def main():
    parser = argparse.ArgumentParser(description="Display Pokedex entries from a specific generation on an e-paper display.")
    parser.add_argument('--generation', type=str, default='', help="Name of the Pokemon generation to display (e.g., 'Gen1', 'Gen2', etc.).")
    parser.add_argument('--pokedex', type=int, default=0, help="Number of the Pokemon's Pokedex entry (e.g., 1, 2, etc.).")

    args = parser.parse_args()
    generation = args.generation
    pokedex = args.pokedex


    game = ''
    if game == '':
        game = DEFAULT_GAMES.get(generation, "")
    if pokedex == 0:
        start, end = POKEMON_RANGES.get(generation, (1, 151))
        pokedex = random.randint(start, end)

    pokedex.display(generation, pokedex)

if __name__ == "__main__":
    main()
