import requests
import sys
from pokemon import Pokemon
from constants import DEFAULT_GAMES, GENERATIONS

def build_pokemon(pokedex_number, generation, version=None, variant=None):
    # Constants
    URL = "https://graphqlpokemon.favware.tech/v7"
    HEADERS = {"Content-Type": "application/json"}

    # Define the GraphQL query with the parameter
    query = _build_query(pokedex_number)

    # Make the POST request with the query
    try:
        response = requests.post(URL, headers=HEADERS, json={"query": query})

        # Check the response status code
        if response.status_code == 200:
            data = response.json()
            pokemon_data = data.get("data", {}).get("getPokemonByDexNumber", {})

            if not pokemon_data:
                print("Pokemon data not found.")
                return None
            pokemon =  _extract_pokemon_from_data(pokedex_number, pokemon_data)
            pokemon.sprite = build_sprite_url(pokedex_number, generation, version, variant)
            return pokemon
        else:
            print("HTTP request failed with status code:", response.status_code)
            return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None
    
def build_sprite_url(pokedex_entry, generation, version=None, variant=None):
    base_url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/"
    
    generation_path = GENERATIONS.get(generation)
    version_path = version or DEFAULT_GAMES.get(generation)
    
    path = f"versions/{generation_path}/{version_path}/"
    
    if variant:
        path += f"{variant}/"
    
    path += f"{pokedex_entry}.png"
    
    return base_url + path


def _build_query(pokedex):
    return f"""
    {{
    getPokemonByDexNumber(number: {pokedex}, offsetFlavorTexts: 8, reverseFlavorTexts: false) {{
        species
        height
        weight
        num
        flavorTexts {{
            flavor
            game
        }}
        types {{
            name
        }}
    }}
    }}
    """

def _extract_pokemon_from_data(pokedex_number, pokemon_data):
    pokemon_name = pokemon_data.get("species", "")
    pokemon_weight = pokemon_data.get("weight", -1)
    pokemon_height = pokemon_data.get("height", -1)
    flavor_texts = pokemon_data.get("flavorTexts", [])
    poke_types = pokemon_data.get("types", [])
    flavor = game = ""
    poke_type = ""


    if flavor_texts:
        # Extract the first flavor text (assuming there's at least one)
        first_flavor_text = flavor_texts[0]
        flavor = first_flavor_text.get("flavor", "")
        game = first_flavor_text.get("game", "")

    if poke_types:
        first_type_text = poke_types[0]
        poke_type = first_type_text.get("name", "")

    return Pokemon(pokedex_number, pokemon_name, poke_type, pokemon_height, pokemon_weight, flavor, game, None)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python get_pokemon_data.py <pokemon_number>")
    else:
        pokemon_number = int(sys.argv[1])

        pokemon = build_pokemon(pokemon_number, "Gen1")
        sprite = build_sprite_url(pokemon_number, "Gen1", "red-blue", "gray")

        if pokemon:
            print(pokemon.species)
            print(pokemon.sprite)

