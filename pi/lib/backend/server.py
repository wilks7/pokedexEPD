from flask import Flask, render_template, request, redirect, url_for, jsonify
from display import display_pokemon, InvalidGenerationError
from lib.constants import GENERATIONS  # Make sure this import is correct

app = Flask(__name__)

@app.route('/pokedex/<int:pokemon_number>/<int:generation>/<string:version>', methods=['GET'])
def get_pokedex_entry(pokemon_number, generation, version):
    try:
        display_pokemon(pokemon_number, generation, version)
        return jsonify(success=True, message="Pokedex entry displayed successfully!")
    except InvalidGenerationError as e:
        return jsonify(success=False, message=str(e)), 400


@app.route('/pokedex', methods=['GET', 'POST'])
def pokedex_form():
    if request.method == 'POST':
        # Handle the form submission
        pokemon_number = request.form.get('pokemon_number')
        generation = int(request.form.get('generation'))  # Convert to integer
        version = request.form.get('version')
        
        # Redirect to the URL structure you specified earlier to display the chosen Pokémon
        return redirect(url_for('get_pokedex_entry', pokemon_number=pokemon_number, generation=generation, version=version))
    
    # If method is GET, serve the HTML form and pass the GENERATIONS constant
    return render_template('pokedex_form.html', generations=GENERATIONS)
