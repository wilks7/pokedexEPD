import requests


def fetch_pokemon(pokedex, generation, version=None, variant=None):
    print(f"Requesting {pokedex} Gen {generation} {version} {variant}")
    data = _fetch_pokemon_data(pokedex, generation)

    pokemon = _extract_pokemon_from_data(pokedex, data)
    
    return pokemon


def _fetch_pokemon_data(pokedex, generation=None):
    URL = "https://graphqlpokemon.favware.tech/v7"
    HEADERS = {"Content-Type": "application/json"}
    
    # Define the GraphQL query with the parameter
    query = _build_query(pokedex)

    try:
        response = requests.post(URL, headers=HEADERS, json={"query": query})
        if response.status_code == 200:
            data = response.json()
            pokemon_data = data.get("data", {}).get("getPokemonByDexNumber", {})

            return pokemon_data
        else:
            print("HTTP Error:", response.status_code)
            return None

    except Exception as error:
        print(f"Error:{error}")
        return None



def _build_query(pokedex, generation=40):
        # getPokemonByDexNumber(number: {pokedex}, offsetFlavorTexts: {0}, reverseFlavorTexts: false, takeFlavorTexts: generation) {{

    return f"""
    {{
    getPokemonByDexNumber(number: {pokedex}, offsetFlavorTexts: {0}, reverseFlavorTexts: false, takeFlavorTexts: {generation}) {{
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
        # print(len(flavor_texts))
        first_flavor_text = flavor_texts[0]
        flavor = first_flavor_text.get("flavor", "")
        game = first_flavor_text.get("game", "")

    if poke_types:
        first_type_text = poke_types[0]
        poke_type = first_type_text.get("name", "")

    return Pokemon(pokedex_number, pokemon_name, poke_type, pokemon_height, pokemon_weight, flavor, game)

class Pokemon:
    def __init__(self, number, species, pokeType, height, weight, flavor, game):
        self.type = pokeType
        self.number = number
        self.species = species
        self.height = height
        self.weight = weight
        self.flavor = flavor
        self.game = game
        self.sprite_url = None
        self.sprite = None

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python get_pokemon_data.py <pokemon_number>")
    else:
        entry = int(sys.argv[1])
        pokemon = fetch_pokemon(entry, 1, "red-blue", "gray")
        if pokemon:
            print(pokemon.species)
            print(pokemon.height)
            print(pokemon.weight)

