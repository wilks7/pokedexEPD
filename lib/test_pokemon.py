from .pokedex.gen1_paper import Gen1

def display_pokemon(resolution, pokedex_entry, generation, version, variant):
    dex = Gen1(resolution, generation, version)
    img = dex.display(pokedex_entry, variant)
    img.show()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Display a Pokemon image.")

    parser.add_argument("--resolution", type=str, default="1872x1404",
                        help="Resolution of the image in WIDTHxHEIGHT format. Default is 1920x1080.")
    parser.add_argument("--generation", type=int, default=1,
                        help="Generation of the Pokemon. Default is 1.")
    parser.add_argument("--version", type=str, default="red-blue",
                        help="Game version. Default is 'red-blue'.")
    parser.add_argument("--pokemon", type=int, default=25,
                        help="Pokedex entry number. Default is 25 (Pikachu).")
    parser.add_argument("--variant", type=str, default=None,
                        help="Pokedex entry number. Default is 25 (Pikachu).")
    # You can add more arguments as needed.

    args = parser.parse_args()

    resolution = tuple(map(int, args.resolution.split('x')))
    generation = args.generation
    version = args.version
    pokemon = args.pokemon
    variant = args.variant

    display_pokemon(resolution, pokemon, generation, version, variant)
