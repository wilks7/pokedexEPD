from flask import Flask, request, jsonify
# from pokedex_display import display_pokemon, InvalidGenerationError
from display import display_pokemon, InvalidGenerationError

app = Flask(__name__)

@app.route('/pokedex/<int:pokemon_number>/<int:generation>/<string:version>', methods=['GET'])
def get_pokedex_entry(pokemon_number, generation, version):
    try:
        display_pokemon(pokemon_number, f"Gen{generation}", version)
        return jsonify(success=True, message="Pokedex entry displayed successfully!")
    except InvalidGenerationError as e:
        return jsonify(success=False, message=str(e)), 400
