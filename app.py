import argparse
from lib import pokedex

def main():
    parser = argparse.ArgumentParser(description="Display Pokedex entries from a specific generation on an e-paper display.")
    parser.add_argument('--generation', type=str, default='', help="Name of the Pokemon generation to display (e.g., 'Gen1', 'Gen2', etc.).")
    parser.add_argument('--pokedex', type=int, default=1, help="Number of the Pokemon's Pokedex entry (e.g., 1, 2, etc.).")

    args = parser.parse_args()

    pokedex.display(args.generation, args.pokedex)

if __name__ == "__main__":
    main()
