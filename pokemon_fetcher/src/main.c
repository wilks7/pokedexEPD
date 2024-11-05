#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "pokemon.h"
#include "network.h"
#include "pokemon_image.h"
#include <ctype.h> // Include this header

// Function to fetch Pokemon data using network and pokemon functions
static Pokemon* fetch_pokemon(int pokedex_number, const char* version) {
    Pokemon* pokemon = pokemon_create();
    if (!pokemon) {
        return NULL;
    }

    // Prepare GraphQL query
    char query[1024];
    snprintf(query, sizeof(query), 
             "{\"query\":\"" POKEMON_QUERY_TEMPLATE "\"}", 
             pokedex_number);

    // Make the request using network functionality
    char* response_data = make_graphql_request(POKEMON_API_ENDPOINT, query);
    if (!response_data) {
        pokemon_free(pokemon);
        return NULL;
    }

    // Parse response
    if (!pokemon_parse_json(response_data, pokemon)) {
        free(response_data);
        pokemon_free(pokemon);
        return NULL;
    }

    // Find the correct generation for this Pokemon
    int generation = 0;
    for (int i = 0; i < GENERATION_COUNT; i++) {
        if (pokedex_number >= GENERATIONS[i].range_start && 
            pokedex_number <= GENERATIONS[i].range_end) {
            generation = i + 1;
            break;
        }
    }

    // Build sprite URL if we found the generation
    if (generation > 0) {
        char* sprite_url = malloc(MAX_URL_LENGTH);
        if (sprite_url) {
            if (pokemon_build_sprite_url(sprite_url, MAX_URL_LENGTH, pokedex_number, 
                                      generation, version, NULL)) {
                pokemon->sprite_url = sprite_url;
            } else {
                free(sprite_url);
            }
        }
    }

    free(response_data);
    return pokemon;
}

void print_pokemon_info(const Pokemon* pokemon) {
    printf("\nPokemon Information:\n");
    printf("------------------\n");
    printf("Name: %s\n", pokemon->name);
    printf("Pokedex ID: %d\n", pokemon->id);
    printf("Height: %d\n", pokemon->height);
    printf("Weight: %d\n", pokemon->weight);
    printf("Description: %s\n", pokemon->description); // Use %s for strings
    printf("Types: ");
    for (int i = 0; i < pokemon->type_count; i++) {
        printf("%s%s", pokemon->types[i], 
               (i < pokemon->type_count - 1) ? ", " : "");
    }
    printf("\nSprite URL: %s\n", pokemon->sprite_url);
}

int main(int argc, char *argv[]) {
    if (argc < 2 || argc > 5) {
        printf("Usage: %s <pokedex_number> [version] [width height]\n", argv[0]);
        printf("Example: %s 25             # Fetches Pikachu with default resolution\n", argv[0]);
        printf("         %s 25 red-blue    # Fetches Pikachu (red-blue version)\n", argv[0]);
        printf("         %s 25 1920 1080   # Fetches Pikachu with 1920x1080 resolution\n", argv[0]);
        printf("\nAvailable versions vary by generation.\n");
        return 1;
    }

    int pokedex = atoi(argv[1]);
    const char* version = NULL;
    int width = 800;  // Default width
    int height = 600; // Default height

    if (argc >= 3) {
        if (isdigit(argv[2][0])) {
            width = atoi(argv[2]);
            height = atoi(argv[3]);
        } else {
            version = argv[2];
            if (argc == 5) {
                width = atoi(argv[3]);
                height = atoi(argv[4]);
            }
        }
    }

    // Initialize network
    if (!network_init()) {
        printf("Failed to initialize network\n");
        return 1;
    }

    // Fetch Pokemon data
    Pokemon* pokemon = fetch_pokemon(pokedex, version);
    if (!pokemon) {
        network_cleanup();
        return 1;
    }

    // Print Pokemon information
    print_pokemon_info(pokemon);

    // Create BMP file with Pokemon's image and name
    char bmp_filename[256];
    snprintf(bmp_filename, sizeof(bmp_filename), "%s.bmp", pokemon->name);
    if (create_pokedex_image(bmp_filename, pokemon, width, height)) {
        printf("BMP file created: %s\n", bmp_filename);
    } else {
        printf("Failed to create BMP file\n");
    }

    // Cleanup
    pokemon_free(pokemon);
    network_cleanup();
    return 0;
}
