from epdlib import Layout
from PIL import Image
from .gen1_layout import Gen1_Layout
from .gen2_layout import Gen2_Layout
from .gen3_layout import Gen3_Layout


Layout_Mapping = {
    1: Gen1_Layout,
    2: Gen2_Layout,
    3: Gen3_Layout,
    4: Gen1_Layout,
    5: Gen1_Layout,
    6: Gen1_Layout,
    7: Gen1_Layout,
    8: Gen1_Layout,
    9: Gen1_Layout,
}

class PokedexLayout(Layout):
    def __init__(self, resolution, mode, generation):
        super().__init__(resolution=resolution, mode=mode)
        self.layout = Layout_Mapping.get(generation, Gen1_Layout)
        
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
