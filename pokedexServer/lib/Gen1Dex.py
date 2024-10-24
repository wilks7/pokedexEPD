from PIL import Image, ImageDraw, ImageFont
from lib.Pokedex import Pokedex
import textwrap

class Gen1(Pokedex):
    def __init__(self, resolution, generation, version):
        super().__init__(generation, version)
        self.width, self.height = resolution
        self.canvas = Image.new("RGB", resolution, "white")
        self.draw = ImageDraw.Draw(self.canvas)
        self.font_path = './font/pokemon_generation_1.ttf'
        self.padding = self.height * 0.05

        # Define sizes for image_block and stats_block as fractions of the overall size
        self.image_block = (self.width // 2, self.height // 2)
        self.stats_block = (self.width // 2, self.height // 2)


    def draw_dex(self, pokedex, variant=None):
        pokemon = self.get_pokemon(pokedex)
        size = self.draw_image(pokedex, variant)

        self.add_stats(pokemon.species, pokemon.type, pokemon.height, pokemon.weight)
        self.add_description(pokemon.flavor)
        self.draw_num(pokedex, size)
        self.add_custom_line()

        return self.canvas

    def draw_image(self, pokedex, variant):
        text_height = (self.height // 2) // 10
        size = min(self.image_block[0], self.image_block[1]) - self.padding * 2 - text_height
        img = self.get_image(pokedex, variant, size)
        
        # Calculate the position to center the image within self.image_block
        x = (self.image_block[0] - img.width) // 2
        y = (self.image_block[1] - img.height) // 2 - text_height
        # y = int(y - self.padding)

        # Paste the image onto the canvas
        self.canvas.paste(img, (x, y))
        
        return size
    

    def draw_num(self, pokedex, image_size):
        # padding = (self.height * 0.2) // 2
        text_height = (self.height // 2) // 10

        text = f"No. {pokedex:03}"

        font_size = self._optimize_font_size(text, image_size, text_height)
        font = ImageFont.truetype(self.font_path, font_size)

        x = (self.image_block[0] - image_size) // 2
        y = (self.image_block[1] + image_size) // 2 - text_height

        self.draw.text((x, y), text, font=font, fill="black")

    def add_custom_line(self, thickness=20, gap_size=128, num_squares=4):
        """Draw a custom line with square patterns at the midway point of the stats block."""
        padding = gap_size // 2
        square_size = 3 * thickness
        square_thickness = thickness // 2

        # Calculate y-coordinate of the midway point of the stats block
        y_mid = self.height // 2
    
        # Starting x-coordinate for right side squares
        x_right = padding

        # Draw the line across the entire width
        self.draw.rectangle([(0, y_mid - thickness//2), (self.width, y_mid + thickness//2)], fill="black")

        for _ in range(num_squares):
            # Draw square on the right side
            square_half_height = square_size // 2
            self.draw.rectangle([(x_right, y_mid - square_half_height), (x_right + square_size, y_mid + square_half_height)], fill="white", outline="black", width=square_thickness)
            x_right += square_size + gap_size

        # Calculate starting x-coordinate for left side squares
        total_width = num_squares * (square_size + gap_size) - gap_size
        x_left = self.width - padding - total_width

        for _ in range(num_squares):
            # Draw square on the left side
            square_half_height = square_size // 2
            self.draw.rectangle([(x_left, y_mid - square_half_height), (x_left + square_size, y_mid + square_half_height)], fill="white", outline="black", width=square_thickness)
            x_left += square_size + gap_size




    def add_stats(self, name, species, weight, height):
        """Add the Pokémon's attributes to the Pokedex canvas left-aligned in the 'stats' block with dynamic font sizes."""
        text_padding = 64
        trailing_padding = 32

        # Determine the available height and width based on the dimensions of stats_block
        available_height = self.stats_block[1] - text_padding * 4  # 3 paddings for 4 text items
        available_width = self.stats_block[0] - trailing_padding   # padding on both sides

        font_size = self._optimize_font_size(name.upper(), available_width, available_height // 4)
        font_size = int(font_size * 0.8)

        # Create font objects
        font = ImageFont.truetype(self.font_path, font_size)

        # Convert weight and height
        weight_lb = self.kg_to_lb(weight)
        height_ft_in = self.meters_to_feet_inches(height)

        # Calculate starting Y coordinate to center the list within the "stats" block
        total_height = 4 * font.getbbox(name.upper())[3] + 3 * text_padding  # assuming all text items have similar height
        y = (self.stats_block[1] - total_height) // 2
        x = self.image_block[0]

        # Draw Name
        self.draw.text((x, y), name.upper(), font=font, fill="black")
        y += font.getbbox(name.upper())[3] + text_padding

        # Draw Species
        self.draw.text((x, y), species, font=font, fill="black")
        y += font.getbbox(species)[3] + text_padding

        # Draw Height
        label = "HT"
        value = height_ft_in
        value_width = font.getbbox(value)[2]
        self.draw.text((x, y), label, font=font, fill="black")
        x_value = self.width - value_width
        self.draw.text((x_value, y), value, font=font, fill="black")
        y += font.getbbox(value)[3] + text_padding

        # Draw Weight
        label = "WT"
        value = weight_lb
        value_width = font.getbbox(value)[2]
        self.draw.text((x, y), label, font=font, fill="black")
        x_value = self.width - value_width
        self.draw.text((x_value, y), value, font=font, fill="black")
        y += font.getbbox(value)[3] + text_padding






    def add_description(self, description, padding=64):
        available_height = self.height // 2 - 2 * padding
        available_width = self.width - 2 * padding

        description_font_size = self._optimize_font_size(description, available_width, available_height)
        description_font = ImageFont.truetype(self.font_path, description_font_size)

        lines = textwrap.wrap(description, width=available_width * len("Sample Text") // description_font.getbbox("Sample Text")[2])
        
        y_text = self.height // 2 + padding
        x = padding

        for line in lines:
            self.draw.text((x, y_text), line, font=description_font, fill="black")
            y_text += description_font.getbbox(line)[3] - description_font.getbbox(line)[1]

    
    def _optimize_font_size(self, text, available_width, available_height, initial_font_size=10):
        font_size = initial_font_size
        while True:
            font_temp = ImageFont.truetype(self.font_path, font_size)
            lines = textwrap.wrap(text, width=available_width * len("Sample Text") // font_temp.getbbox("Sample Text")[2])
            total_text_height = sum([font_temp.getbbox(line)[3] - font_temp.getbbox(line)[1] for line in lines])

            if total_text_height > available_height or any([font_temp.getbbox(line)[2] > available_width for line in lines]):
                return font_size - 1

            font_size += 1

    def kg_to_lb(self, weight_kg):
        weight_lb = float(weight_kg*0.1) * 2.20462
        return f'{weight_lb:.1f} l b'

    def meters_to_feet_inches(self, height_m):
        total_inches = height_m * 39.3701
        feet = int(total_inches // 12)
        inches = round(total_inches % 12)
        return f"{feet}' {inches:02}\""



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Fetch and display Pokémon data from PokeAPI.")
    
    parser.add_argument("--pokedex", type=int, default=1, help="Pokédex entry number (default: 1)")
    parser.add_argument("--generation", type=int, default=1)
    parser.add_argument("--version", type=str, default="red-blue", help="Game version (default: None)")
    parser.add_argument("--variant", type=str, default=None, help="Sprite variant (default: None)")
    parser.add_argument("--resolution", type=str, default="1920x1080")
    
    args = parser.parse_args()

    resolution = tuple(map(int, args.resolution.split('x')))

    dex = Gen1(resolution, args.generation, args.version)

    img = dex.draw_dex(args.pokedex)

    img.show()
