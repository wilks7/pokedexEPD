from flask import Flask, request
from pokedex_display import display_pokemon, InvalidGenerationError

app = Flask(__name__)

@app.route('/pokedex', methods=['POST'])
def change_pokedex_entry():
    pokemon_number = request.form.get('pokemon_number')
    generation = request.form.get('generation')
    version = request.form.get('version', None)  # Default to None if not provided

    if not pokemon_number or not generation:
        return "Missing parameters!", 400

    try:
        display_pokemon(int(pokemon_number), generation, version)
        return "Pokedex entry changed!", 200
    except InvalidGenerationError as e:
        return str(e), 400

if __name__ == "__main__":
    app.run()
