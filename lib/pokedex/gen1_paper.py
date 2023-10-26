from PIL import Image, ImageDraw, ImageFont
from .pokedex_helper import Pokedex
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

    def display(self, pokedex, variant=None):
        return self.draw_dex(pokedex, variant)


    def draw_dex(self, pokedex, variant=None):
        pokemon = self.get_pokemon(pokedex)
        size = self.draw_image(pokedex, variant)
        self.add_stats(pokemon.species, pokemon.type, pokemon.height, pokemon.weight)
        self.add_description(pokemon.flavor)
        self.draw_num(25, size)
        self.add_custom_line()
        return self.canvas

    def draw_image(self, pokedex, variant):
        text_height = (self.height // 2) // 10
        print('Padding', self.padding)
        size = min(self.image_block[0], self.image_block[1]) - self.padding * 2 - text_height
        print('Image', size)
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
        print("Height", text_height)

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

        # Attributes with converted values
        attributes = [
            (name.upper(), font),
            (species, font),
            (f"HT {height_ft_in}", font),
            (f"WT {weight_lb}", font)
        ]

        # Compute the total height of all text items plus padding between them
        total_height = sum([font.getbbox(attr)[3] for attr, font in attributes]) + text_padding * (len(attributes) - 1)

        # Calculate starting Y coordinate to center the list within the "stats" block
        y = (self.stats_block[1] - total_height) // 2
        x = self.image_block[0]

        for attr, font in attributes:
            if "HT" in attr or "WT" in attr:
                # Separate label (either HT or WT) and its value
                label, value = attr.split(maxsplit=1)

                # Calculate the width of the value using the font's getbbox() method
                value_width = font.getbbox(value)[2]

                # Draw the label (either HT or WT) left-aligned to self.image_block[0]
                self.draw.text((x, y), label, font=font, fill="black")

                # Calculate the X position for the value to be right-aligned to self.width
                x_value = self.width - value_width

                # Draw the value at the calculated position
                self.draw.text((x_value, y), value, font=font, fill="black")
            else:
                # Draw the attribute on the canvas with its corresponding font
                self.draw.text((x, y), attr, font=font, fill="black")
            
            # Adjust Y coordinate for the next attribute: increase by the height of the current text and add padding
            y += font.getbbox(attr)[3] + text_padding





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
        weight_lb = float(weight_kg) * 2.20462
        return f'{weight_lb:.1f} l b'

    def meters_to_feet_inches(self, height_m):
        total_inches = height_m * 39.3701
        feet = int(total_inches // 12)
        inches = round(total_inches % 12)
        return f"{feet}' {inches:02}\""



if __name__ == "__main__":
    resolution = (1920, 1080)
    dex = Gen1(resolution, 1, 'yellow')
    img = dex.display(25)
    img.show()
    # img.save("output_pokedex.png")