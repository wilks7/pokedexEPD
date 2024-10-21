from lib.pokedex.gen1_paper import Gen1

def display_pokemon(resolution, pokedex_entry, generation, version, variant):
    dex = Gen1(resolution, generation, version)
    img = dex.display(pokedex_entry, variant)
    img.show()

def check_generation(range, generation, version=None, variant=None):
    for i in range:
        dex = Gen1(resolution, generation, version)
        img = None
        img = dex.display(i, variant)

    img.show()

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

    display_pokemon(resolution, pokemon, generation, version, variant)
    # check_generation(range(152,252 ), generation, version, variant)
