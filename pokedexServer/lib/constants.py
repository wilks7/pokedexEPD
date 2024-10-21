# Define Generations, Pokedex Ranges, Versions, and Variants
GENERATIONS = {
    1: {
        "title": "Generation-I",
        "range": (1, 151),
        "versions": {
            "red-blue": ["back", "gray", "transparent", "back-gray"],
            "yellow": ["back", "gbc", "gray", "transparent", "back-gbc", "back-gray", "back-transparent"]
        }
    },
    2: {
        "title": "Generation-II",
        "range": (152, 251),
        "versions": {
            "gold": ["back", "shiny", "transparent", "back-shiny"],
            "silver": ["back", "shiny", "transparent", "back-shiny"],
            "crystal": ["back", "shiny", "back-shiny", "transparent", "transparent-shiny", "back-transparent", "back-transparent-shiny"]
        }
    },
    3: {
        "title": "Generation-III",
        "range": (252, 386),
        "versions": {
            "ruby-sapphire": ["back", "shiny", "back-shiny"],
            "emerald": ["shiny"],
            "firered-leafgreen": ["back", "shiny", "back-shiny"]
        }
    },
    4: {
        "title": "Generation-IV",
        "range": (387, 493),
        "versions": {
            "diamond-pearl": ["back", "female", "shiny", "back-female", "back-shiny", "shiny-female"],
            "platinum": ["back", "female", "shiny", "back-female", "back-shiny", "shiny-female"],
            "heartgold-soulsilver": ["back", "female", "shiny", "back-female", "back-shiny", "shiny-female"]
        }
    },
    5: {
        "title": "Generation-V",
        "range": (494, 649),
        "versions": {
            "black-white": ["back", "female", "shiny", "back-female", "back-shiny", "shiny-female", "animated"]
        }
    },
    6: {
        "title": "Generation-VI",
        "range": (650, 721),
        "versions": {
            "x-y": ["female", "shiny", "shiny-female"],
            "omegaruby-alphasapphire": ["female", "shiny", "shiny-female"]
        }
    },
    7: {
        "title": "Generation-VII",
        "range": (722, 809),
        "versions": {
            "sun-moon": ["female", "shiny", "shiny-female"],
            "ultra-sun-ultra-moon": ["female", "shiny", "shiny-female"],
            "icons": []
        }
    },
    8: {
        "title": "Generation-VIII",
        "range": (810, 898),
        "versions": {
            "sword-shield": [],
            "icons": ["female"]
        }
    }
}

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

OTHER_SPRITE_CATEGORIES = ["dream-world", "home", "official-artwork", "showdown"]

DEFAULT_VERSIONS = {
    1: "red-blue",
    2: "silver",
    3: "ruby-sapphire",
    4: "diamond-pearl",
    5: "black-white",
    6: "x-y",
    7: "ultra-sun-ultra-moon",
    8: "icons"
}