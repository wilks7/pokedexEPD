from .lib.pokedex.api.api import build_pokemon
from .lib.pokedex.drawSprite import fetchSprite
from .lib.constants import POKEMON_RANGES


def display(self, pokedex, generation, version=None, variant=None):
    print(f"Requesting {pokedex} Gen {generation}")
    pokemon = build_pokemon(pokedex, generation, version, variant)
    img = fetchSprite(pokemon.sprite, self.height)
    
    print(pokemon.species)
    print(pokemon.sprite)

    self.layout.updatePokemon(pokemon, img)
    self.screen.writeEPD(self.layout.concat())

def slideshow(self, generation, sorted=True, delay=10):
    start, end = POKEMON_RANGES.get(generation, (1, 151))
    pokedex_entries = list(range(start, end + 1))
    
    if not sorted:
        random.shuffle(pokedex_entries)

    for pokedex in pokedex_entries:
        self.display(pokedex,generation)
        sleep(delay)
    # self.screen.clearEPD()