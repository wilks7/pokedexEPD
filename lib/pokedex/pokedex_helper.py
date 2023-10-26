from PIL import Image
from .pokemon_api import fetch_pokemon
from . pokemon_sprite import fetch_sprite
from abc import abstractmethod

class Pokedex:
    def __init__(self, generation, version):
        self.generation = generation
        self.version = version

    def get_pokemon(self, pokedex):
        pokemon = fetch_pokemon(pokedex, self.generation, self.version)
        return pokemon
    
    def get_image(self, pokedex, size=None):
        sprite = fetch_sprite(pokedex, self.generation, self.version, None)
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
    def draw_dex(self, pokedex, variant=None):
        pass        
