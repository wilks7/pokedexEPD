from epdlib import Layout
from PIL import Image
from pokedex_api import get_pokemon_data
from pokedex_api import Pokemon
import urllib.request 
from pokeSprite import get_pokemon_sprite
import requests

class PokedexLayout(Layout):
    def __init__(self, resolution, mode):
        super().__init__(resolution=resolution, mode=mode)
        self.layout = {
            'image_block': {
                'type':            'ImageBlock',
                'height':          .5,
                'width':           .5,
                # 'hcenter':         True,
                # 'vcenter':         False,
                'abs_coordinates': (0, 0),
                # use absolute position declared in this block for the X
                # use the bottom of the text_block as the Y position for this block
                'relative':        False,
                'bkground':        'WHITE',
                'fill':            'BLACK',
                'mode':            'L'
            },
            'pokemon_name': {
                 'type': 'TextBlock',
                 'mode': 'L',
                 'image': False,
                 'max_lines': 1,
                 'width': .5,
                 'height': .1,
                 'font': './font/pokemon_generation_1.ttf', # path to font file - this font is included
                 'abs_coordinates': (None, 0),
                 'relative': ['image_block', 'pokemon_name'],
                 'padding': 10,
                 'hcenter': False,
                 'vcenter': False,
                 'align': 'left',
                 'rgb_support': True
             },
             'pokemon_type': {
                 'type': 'TextBlock',
                 'mode': 'L',
                 'image': False,
                 'max_lines': 1,
                 'width': 1,
                 'height': .09,
                 'font': './font/pokemon_generation_1.ttf', # path to font file - this font is included
                 'abs_coordinates': (None, None),
                 'relative': ['image_block', 'pokemon_name'],
                 'padding': 10,
                 'hcenter': False,
                 'vcenter': False,
                 'align': 'left',
                 'rgb_support': True
             },    
             'pokemon_height': {
                 'type': 'TextBlock',
                 'mode': 'L',
                 'image': False,
                 'max_lines': 1,
                 'width': .5,
                 'height': .07,
                 'font': './font/pokemon_generation_1.ttf', # path to font file - this font is included
                 'abs_coordinates': (None, None),
                 'relative': ['image_block', 'pokemon_type'],
                 'padding': 10,
                 'hcenter': False,
                 'vcenter': False,
                 'align': 'left',
                 'rgb_support': True
             }, 
            'pokemon_weight': {
                 'type': 'TextBlock',
                 'mode': 'L',
                 'image': False,
                 'max_lines': 1,
                 'width': .5,
                 'height': .07,
                 'font': './font/pokemon_generation_1.ttf', # path to font file - this font is included
                 'abs_coordinates': (None, None),
                 'relative': ['image_block', 'pokemon_height'],
                 'padding': 10,
                 'hcenter': False,
                 'vcenter': False,
                 'align': 'left',
                 'rgb_support': True
             }, 
            'pokedex_number': {
                 'type': 'TextBlock',
                 'mode': 'L',
                 'image': False,
                 'max_lines': 1,
                 'width': .5,
                 'height': .07,
                 'font': './font/pokemon_generation_1.ttf', # path to font file - this font is included
                 'abs_coordinates': (None, None),
                 'relative': ['image_block', 'pokemon_weight'],
                 'padding': 10,
                 'hcenter': False,
                 'vcenter': False,
                 'align': 'left',
                 'rgb_support': True
             }, 
            'pokedex_entry': {
                'type': 'TextBlock',
                'width': 1,
                'height': .5,
                'abs_coordinates': (0, None),
                'relative': ('pokedex_entry', 'image_block'),
                'mode' : "L", # L for 8 bit color
                # Optional
                'font': './font/pokemon_generation_1.ttf', # path to font file - this font is included
                'max_lines': 6,              # number of lines of text
                'textwrap' : True,
                'hcenter': False,
                'vcenter': False,
                'padding': 100,
                'border_config': {'fill': 0, 'width': 16, 'sides': ['top']},

                'font_size': 12
            }
        }



    def resize_image(self, img):
        width, height = self.resolution
        desired_height = int(height / 2)
        # with Image.open(image_path) as img:
        original_width, original_height = img.size
        aspect_ratio = original_width / original_height
        new_width = int(desired_height * aspect_ratio)
        img = img.resize((new_width, desired_height), Image.ANTIALIAS)
        return img

        
    def updatePokemon(self, pokemon):
        self.updateImage(pokemon)
        self.updateStats(pokemon)
        self.updateText(pokemon.flavor)

    def getSprite(self, pokemon):
        (dir, file) = get_pokemon_sprite("Gen1", "red-blue", "gray", str(pokemon.number))
        path = f'./{dir}/{file}'
        print(path)
        img = Image.open(path)
        return img

    def pullImage(self, pokemon):
        url = pokemon.sprite
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            path = "poke_image.gif"
            with open(path, 'wb') as f:
                f.write(response.content)
            my_img = Image.open(path)
            return my_img
        else:
            print(f"Error fetching image: {response.status_code}")
            return None

    def updateImage(self, pokemon):

        img = self.getSprite(pokemon)
        # img = self.pullImage(pokemon)

        img = self.resize_image(img)
        self.update_contents({'image_block': img})

        # image_path = f'./images/{number}_small.png'
        # self.update_contents({'image_block': resized_image})


    def updateStats(self, pokemon):
        # string = f'{pokemon.species} {pokemon.height} {pokemon.weight}'
        self.update_contents({'pokemon_name': pokemon.species.upper()})
        self.update_contents({'pokemon_type': pokemon.type})

        weight = f'WT: {pokemon.weight}'
        height = f'HT: {pokemon.height}'
        number = f'$ {pokemon.number}'
        self.update_contents({'pokemon_height': height})
        self.update_contents({'pokemon_weight': weight})
        self.update_contents({'pokedex_number': number})


    def updateText(self, text):
        self.update_contents({'pokedex_entry': text})



    def generate_layout(self):
        return self.concat()
