import random
import constants

def get_pokemon_sprite(gen, game, gray, pokemon_id):
    """
    Returns the path to the desired Pokémon sprite.

    Args:
    - gen (str): The generation (e.g., "Gen1").
    - game (str, optional): The game within the generation (e.g., "red-blue"). Defaults to the primary game for the generation.
    - pokemon_id (int, optional): The ID of the Pokémon. Defaults to a random Pokémon within the generation.

    Returns:
    - str: The path to the Pokémon sprite.
    """
    
    if game is None:
        game = constants.DEFAULT_GAMES.get(gen, "")
    if pokemon_id is None:
        start, end = constants.POKEMON_RANGES.get(gen, (1, 151))
        pokemon_id = random.randint(start, end)
    
    directory = f'images/{gen}/{game}'
    if gray == "gray" and gen == "Gen1":
        directory = f'images/{gen}/{game}/gray'

    filename = f'{str(pokemon_id).zfill(4)}.png'

    return (directory, filename)
