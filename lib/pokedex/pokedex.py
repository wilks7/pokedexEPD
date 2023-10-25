from PIL import Image
from ..api.pokemon_api import fetch_pokemon
from ..api.sprite import fetch_sprite

class PokedexHelper:
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


    def _resize_image(self, img, height):
        desired_height = int(height / 2)
    
        original_width, original_height = img.size
        aspect_ratio = original_width / original_height
        new_width = int(desired_height * aspect_ratio)
        
        dimensions = (new_width, desired_height)
        img = img.resize(dimensions, Image.NEAREST)

        return img
