import configargparse
import configparser
import os
import sys
from config import get_config

def main():
    current_directory = os.getcwd()
    config_file = os.path.join(current_directory, 'config.ini')
    
    arg_parser = configargparse.ArgParser(
        default_config_files=[config_file] if config_file else [],
        description="Display Pokedex entries from a specific generation on an e-paper display."
    )


    arg_parser.add_argument('--pokedex', '-p', type=int, default=None, help="Number of the Pokemon's Pokedex entry (e.g., 1, 2, etc.).")
    arg_parser.add_argument('--generation','-gen', type=int, required=True, help="Name of the Pokemon generation to display (e.g., 'Gen1', 'Gen2', etc.).")
    arg_parser.add_argument('--version', type=str, default=None, help="Version game of the generation.")

    arg_parser.add_argument('--slideshow', action='store_true', help="Start a slideshow to display the Pokemon entries")

    arg_parser.add_argument('--config', is_config_file=True, help='Config file path')

    args = arg_parser.parse_known_args()





if __name__ == "__main__":
    main()
