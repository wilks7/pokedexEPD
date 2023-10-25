
import requests
from PIL import Image
from io import BytesIO

def fetch_sprite(pokedex_entry, generation, version=None, variant=None):
    url = build_sprite_url(pokedex_entry, generation, version, variant)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))

        return img
    else:
        print(f"Error fetching image: {response.status_code}")
        print(url)
        return None

def build_sprite_url(pokedex_entry, generation, version=None, variant=None):
    base_url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/"
    if generation is None:
        generation = 8
    if generation < 1 or generation > 9:
        return ""

    roman_numeral = _toRoman(generation)

    generation_path = f"generation-{roman_numeral}"
    version_path = version or DEFAULT_GAMES.get(generation)
    
    path = f"versions/{generation_path}/{version_path}/"

    if variant:
        if version_path in GAME_VARIANTS:
            valid_variants = GAME_VARIANTS[version_path]
            if variant not in valid_variants:
                print(f"Invalid variant '{variant}' for game version '{version_path}' using default")
            else:
                path += f"{variant}/"
    
    path += f"{pokedex_entry}.png"
    
    return base_url + path

def _toRoman(number):
    if number < 1 or number > 9:
        raise ValueError("Number must be between 1 and 9")
    roman_numerals = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix"]
    return roman_numerals[number - 1]


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

DEFAULT_GAMES = {
    1: "red-blue",
    2: "silver",
    3: "ruby-sapphire",
    4: "diamond-pearl",
    5: "black-white",
    6: "x-y",
    7: "ultra-sun-ultra-moon",
    8: "icons"
}

if __name__ == "__main__":
    import sys
    import tkinter as tk
    from PIL import ImageTk

    if len(sys.argv) != 4:
        print("Usage: python get_pokemon_data.py <pokemon_number> <generation> <size>")
    else:
        pokemon = int(sys.argv[1])
        generation = int(sys.argv[2])
        size = int(sys.argv[3])

        root = tk.Tk()
        root.title("Image Viewer")

        img = fetchSprite(pokemon, generation)

        desired_height = int(size / 2)
        # with Image.open(image_path) as img:
        original_width, original_height = img.size
        aspect_ratio = original_width / original_height
        new_width = int(desired_height * aspect_ratio)
        img = img.resize((new_width, desired_height), Image.NEAREST)

        photo = ImageTk.PhotoImage(img)
        label = tk.Label(root, image=photo)
        label.pack()
        label.img = photo
        root.mainloop()
