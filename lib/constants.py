# constants.py


GENERATIONS = {
    "Gen1": "generation-i",
    "Gen2": "generation-ii",
    "Gen3": "generation-iii",
    "Gen4": "generation-iv",
    "Gen5": "generation-v",
    "Gen6": "generation-vi",
    "Gen7": "generation-vii",
    "Gen8": "generation-viii"
}

# Mapping of generations to their default games
DEFAULT_GAMES = {
    "Gen1": "red-blue",
    "Gen2": "crystal",
    "Gen3": "ruby-sapphire",
    "Gen4": "diamond-pearl",
    "Gen5": "black-white",
    "Gen6": "x-y",
    "Gen7": "ultra-sun-ultra-moon",
    "Gen8": "icons"
}

# Mapping of generations to the range of Pokémon they include
POKEMON_RANGES = {
    "Gen1": (1, 151),
    "Gen2": (152, 251),
    "Gen3": (252, 386),
    "Gen4": (387, 493),
    "Gen5": (494, 649),
    "Gen6": (650, 721),
    "Gen7": (722, 809),
    "Gen8": (810, 898)  # Assuming Gen 8 goes up to #898, adjust as needed
}

# Mapping of games (versions) to their available sprite variants
GAME_VARIANTS = {
    "red-blue": ["back", "gray", "transparent", "back-gray"],
    "yellow": ["back", "gbc", "gray", "transparent", "back-gbc", "back-gray", "back-transparent"],
    "crystal": ["back", "shiny", "back-shiny", "transparent", "transparent-shiny", "back-transparent", "back-transparent-shiny"],
    "gold": ["back", "shiny", "transparent", "back-shiny"],
    "silver": ["back", "shiny", "transparent", "back-shiny"],
    "ruby-sapphire": ["back", "shiny", "back-shiny"],
    "emerald": ["shiny"],
    "fire-red-leaf-green": ["back", "shiny", "back-shiny"],
    "diamond-pearl": ["back", "female", "shiny", "back-female", "back-shiny", "shiny-female"],
    "platinum": ["back", "female", "shiny", "back-female", "back-shiny", "shiny-female"],
    "heart-gold-soul-silver": ["back", "female", "shiny", "back-female", "back-shiny", "shiny-female"],
    "black-white": ["back", "female", "shiny", "back-female", "back-shiny", "shiny-female", "animated"],
    "x-y": ["female", "shiny", "shiny-female"],
    "omega-ruby-alpha-sapphire": ["female", "shiny", "shiny-female"],
    "ultra-sun-ultra-moon": ["female", "shiny", "shiny-female"],
    "icons": ["female"]
}

# Other sprite categories
OTHER_SPRITE_CATEGORIES = ["dream-world", "home", "official-artwork", "showdown"]


