
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

    def __str__(self):
        return (f"Number: {self.number}\n"
                f"Species: {self.species}\n"
                f"Type: {self.type}\n"
                f"Height: {self.height}\n"
                f"Weight: {self.weight}\n"
                f"Flavor: {self.flavor}\n"
                f"Game: {self.game}\n")