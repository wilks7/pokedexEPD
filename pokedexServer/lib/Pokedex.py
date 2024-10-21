from PIL import Image
from abc import abstractmethod
from lib.api import fetch_pokemon, fetch_sprite

class Pokedex:
    def __init__(self, generation, version):
        self.generation = generation
        self.version = version

    def get_pokemon(self, pokedex):
        pokemon = fetch_pokemon(pokedex, self.generation, self.version)
        return pokemon
    
    def get_image(self, pokedex, variant=None, size=None):
        sprite = fetch_sprite(pokedex, self.generation, self.version, variant)
        if size is None:
            return sprite
        else:
            return self._resize_image(sprite, size)


    def _resize_image(self, img, size):
        desired_height = int(size)
    
        original_width, original_height = img.size
        aspect_ratio = original_width / original_height
        new_width = int(desired_height * aspect_ratio)
        
        dimensions = (new_width, desired_height)
        img = img.resize(dimensions, Image.NEAREST)

        return img
    
    @abstractmethod
    def draw_dex(self, pokedex, variant=None) -> Image:
        pass        


class PokemonRequest:
    generation: int
    entry: tuple
    version: str
    variant: str


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Fetch and display Pokémon data from PokeAPI.")

    # Add arguments for the Pokédex, generation, version, variant, and size
    parser.add_argument("--pokedex", type=int, default=1, help="Pokédex entry number (default: 1)")
    parser.add_argument("--generation", type=int, default=1, help="Generation number (default: 1)")
    parser.add_argument("--version", type=str, default=None, help="Game version (default: None)")
    parser.add_argument("--variant", type=str, default=None, help="Sprite variant (default: None)")
    parser.add_argument("--size", type=int, default=None, help="Desired height of the sprite image (default: None)")

    # Parse the arguments
    args = parser.parse_args()

    class ConcretePokedex(Pokedex):
        def draw_dex(self, pokedex, variant=None, size=None):
            # Get Pokémon data and image
            pokemon = self.get_pokemon(pokedex)
            sprite = self.get_image(pokedex, variant, size)

            # Print Pokémon data
            if pokemon:
                print(pokemon)

            # Show the Pokémon sprite if available
            if sprite:
                sprite.show()
    # Create an instance of ConcretePokedex
    pokedex = ConcretePokedex(args.generation, args.version)

    # Fetch Pokémon data and display the sprite
    pokedex.draw_dex(args.pokedex, variant=args.variant, size=args.size)