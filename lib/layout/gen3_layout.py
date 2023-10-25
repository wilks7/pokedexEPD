
Gen3_Layout = {
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