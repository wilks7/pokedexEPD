import http.client
import json
from urllib.parse import urlparse
from io import BytesIO    
from PIL import Image

from lib.Pokemon import Pokemon
from lib.constants import GENERATIONS

def fetch_pokemon(pokedex, generation, version=None, variant=None):
    print(f"Requesting Pokedex: {pokedex} Gen {generation}")
    data = _fetch_pokemon_data(pokedex, generation)

    if data is None:
        print("Failed to fetch Pokemon data.")
        return None

    pokemon = _extract_pokemon_from_data(pokedex, data)
    return pokemon


def _fetch_pokemon_data(pokedex, generation=None):
    URL = "graphqlpokemon.favware.tech"
    HEADERS = {"Content-Type": "application/json"}
    
    # Define the GraphQL query with the parameter
    query = _build_query(pokedex, generation)

    # Prepare the connection and the request
    try:
        connection = http.client.HTTPSConnection(URL)
        request_body = json.dumps({"query": query})
        connection.request("POST", "/v8", body=request_body, headers=HEADERS)

        response = connection.getresponse()

        if response.status == 200:
            data = json.loads(response.read().decode())
            return data.get("data", {}).get("getPokemonByDexNumber", {})
        else:
            print("HTTP Error:", response.status)
            return None

    except Exception as error:
        print(f"Error: {error}")
        return None


def _build_query(pokedex, generation=40):
    return f"""
    {{
        getPokemonByDexNumber(number: {pokedex}, offsetFlavorTexts: 0, reverseFlavorTexts: false, takeFlavorTexts: {generation}) {{
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
    pokemon_name = pokemon_data.get("species", "Unknown")
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

    return Pokemon(pokedex_number, pokemon_name, poke_type, pokemon_height, pokemon_weight, flavor, game)


##################
# Sprite API #
##################



def fetch_sprite(pokedex_entry: int, generation: int, version: str = None, variant: str = None):
    url = build_sprite_url(pokedex_entry, generation, version, variant)
    
    parsed_url = urlparse(url)
    if not parsed_url.netloc:
        print("Invalid URL:", url)
        return None

    try:
        connection = http.client.HTTPSConnection(parsed_url.netloc)
        HEADERS = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}    
        connection.request("GET", parsed_url.path, headers=HEADERS)
        
        response = connection.getresponse()

        if response.status == 200:
            bytes_data = BytesIO(response.read())
            return Image.open(bytes_data)
        else:
            print(f"Failed to fetch sprite: HTTP {response.status}, URL: {url}")
            return None

    except Exception as error:
        print(f"Error fetching sprite: {error}")
        return None


def build_sprite_url(pokedex_entry, generation: int, version=None, variant=None):
    base_url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/"

    gen_info = GENERATIONS.get(generation)
    if not gen_info:
        raise ValueError(f"Invalid generation: {generation}")

    generation_path = gen_info["title"].lower()
    version_path = version or next(iter(gen_info["versions"]))
    variant_path = _variant(gen_info, version_path, variant)

    path = f"versions/{generation_path}/{version_path}/{variant_path}{pokedex_entry}.png"
    return base_url + path


def _variant(gen_info, version_path: str, variant: str) -> str:
    if variant and variant in gen_info["versions"].get(version_path, []):
        return f"{variant}/"
    return ""


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Fetch and display a Pokémon sprite from PokeAPI.")
    
    # Add arguments for the Pokédex, generation, version, and variant
    parser.add_argument("--pokedex", type=int, default=1, help="Pokédex entry number (default: 1)")
    parser.add_argument("--generation", type=int, default=1, help="Generation number (default: 1)")
    parser.add_argument("--version", type=str, default=None, help="Game version (default: None)")
    parser.add_argument("--variant", type=str, default=None, help="Sprite variant (default: None)")

    # Parse the arguments
    args = parser.parse_args()

    # Fetch the sprite with provided arguments
    pokemon = fetch_pokemon(args.pokedex, args.generation)
    if pokemon:
        print(pokemon)

    sprite = fetch_sprite(args.pokedex, args.generation, args.version, args.variant)
    if sprite:
        sprite.show()  # Display the fetched sprite
