import configargparse
import os
import sys
from display import display_pokemon, start_slideshow, InvalidGenerationError

import random
from lib.constants import POKEMON_RANGES
from lib.backend import app  # Import Flask app from server.py


def main():
    config_file = os.path.join(os.getcwd(), 'omni-epd.ini')
    
    parser = configargparse.ArgParser(
        default_config_files=[config_file] if config_file else [],
        description="Display Pokedex entries from a specific generation on an e-paper display."
    )

    parser.add_argument('--pokedex', '-p', type=int, default=None, help="Number of the Pokemon's Pokedex entry (e.g., 1, 2, etc.).")
    parser.add_argument('--generation', '-gen', type=int, required=True, help="Name of the Pokemon generation to display (e.g., 'Gen1', 'Gen2', etc.).")
    parser.add_argument('--version', type=str, default=None, help="Version game of the generation.")
    parser.add_argument('--slideshow', action='store_true', help="Start a slideshow to display the Pokemon entries")
    parser.add_argument('--config', is_config_file=True, help='Config file path')

    args, _ = parser.parse_known_args()

    try:
        if args.slideshow:
            start_slideshow(args.generation, args.version)
        else:
            pokedex = args.pokedex or random.randint(*POKEMON_RANGES[args.generation])
            display_pokemon(pokedex, args.generation, args.version)
            app.run(host='0.0.0.0', port=5000)  # Listening on all interfaces

    except InvalidGenerationError as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
