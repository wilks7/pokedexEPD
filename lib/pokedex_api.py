import requests
import sys

class Pokemon:
    def __init__(self, number, species, pokeType, height, weight, flavor, game, sprite):
        self.type = pokeType
        self.number = number
        self.species = species
        self.height = height
        self.weight = weight
        self.flavor = flavor
        self.game = game
        self.sprite = sprite

def get_pokemon_data(pokedex_number):
    # Specify the GraphQL endpoint
    url = "https://graphqlpokemon.favware.tech/v7"

    # Set request headers for GraphQL
    headers = {"Content-Type": "application/json"}

    # Define the GraphQL query with the parameter
    query = f"""
    {{
      getPokemonByDexNumber(number: {pokedex_number}, offsetFlavorTexts: 1, reverseFlavorTexts: false) {{
        species
        height
        weight
        num
        sprite
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

    # Make the POST request with the query
    response = requests.post(url, headers=headers, json={"query": query})

    # Check the response status code
    if response.status_code == 200:
        data = response.json()
        pokemon_data = data.get("data", {}).get("getPokemonByDexNumber", {})

        if not pokemon_data:
            print("Pokemon data not found.")
            return None

        pokemon_name = pokemon_data.get("species", "")
        pokemon_weight = pokemon_data.get("weight", -1)
        pokemon_height = pokemon_data.get("height", -1)
        pokemon_sprite = pokemon_data.get("sprite", "")

        flavor_texts = pokemon_data.get("flavorTexts", [])
        pokeTypes = pokemon_data.get("types", [])
        flavor = game = ""
        poke_type = ""

        if flavor_texts:
            # Extract the first flavor text (assuming there's at least one)
            first_flavor_text = flavor_texts[0]
            flavor = first_flavor_text.get("flavor", "")
            game = first_flavor_text.get("game", "")

        if pokeTypes:
            first_type_text = pokeTypes[0]
            poke_type = first_type_text.get("name", "")

        pokemon = Pokemon(pokedex_number, pokemon_name, poke_type, pokemon_height, pokemon_weight, flavor, game, pokemon_sprite)
        print("Fetched:", pokemon.species)
        return pokemon
    else:
        print("HTTP request failed with status code:", response.status_code)
        return None
    


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python get_pokemon_data.py <pokemon_number>")
    else:
        pokemon_number = int(sys.argv[1])
        pokemon = get_pokemon_data(pokemon_number)

        if pokemon:
            print("Pokemon Name:", pokemon.species)
            print("Pokedex Weight:", pokemon.weight)
            print("Pokedex Height:", pokemon.height)
            print("Flavor:", pokemon.flavor)
            print("Game:", pokemon.game)
