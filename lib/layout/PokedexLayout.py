from epdlib import Layout
from PIL import Image
from .gen1_layout import Gen1_Layout

class PokedexLayout(Layout):
    def __init__(self, resolution, mode, generation):
        super().__init__(resolution=resolution, mode=mode)
        # if generation == 1:
        self.layout = Gen1_Layout

        
    def updatePokemon(self, pokemon, img):
        self.update_contents({'image_block': img})
        
        name = pokemon.species.upper()
        type = pokemon.type
        weight = f'WT: {pokemon.weight}'
        height = f'HT: {pokemon.height}'
        number = f'$ {pokemon.number}'

        self.update_contents({'pokemon_name': name})
        self.update_contents({'pokemon_type': type})
        self.update_contents({'pokemon_height': height})
        self.update_contents({'pokemon_weight': weight})
        self.update_contents({'pokedex_number': number})

        self.update_contents({'pokedex_entry': pokemon.flavor})
