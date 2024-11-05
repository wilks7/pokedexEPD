#ifndef POKEMON_H
#define POKEMON_H

#include <stdbool.h>
#include <stdlib.h>

// Core Pokemon data structure
typedef struct {
    char* name;
    char* sprite_url;
    int id;
    int height;
    int weight;
    char** types;
    int type_count;
    char* description;
} Pokemon;

// Constant Definitions
#define MAX_VERSIONS 5
#define MAX_VARIANTS 10
#define MAX_VERSION_NAME 50
#define MAX_VARIANT_NAME 30
#define MAX_URL_LENGTH 512

// API Constants
#define POKEMON_API_ENDPOINT "https://graphqlpokemon.favware.tech/v8"
#define POKEMON_CONTENT_TYPE "application/json"
#define SPRITE_BASE_URL "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon"

// GraphQL Query Templates
#define POKEMON_QUERY_TEMPLATE \
    "{" \
    "  getPokemonByDexNumber(number: %d) {" \
    "    species" \
    "    height" \
    "    weight" \
    "    num" \
    "    types {" \
    "      name" \
    "    }" \
    "    flavorTexts {" \
    "      flavor" \
    "      game" \
    "    }" \
    "  }" \
    "}"

// Sprite Data Structures
typedef struct {
    char name[MAX_VERSION_NAME];
    char variants[MAX_VARIANTS][MAX_VARIANT_NAME];
    int variant_count;
} version_info_t;

typedef struct {
    char title[20];
    int range_start;
    int range_end;
    version_info_t versions[MAX_VERSIONS];
    int version_count;
} generation_info_t;

// Generation Constants
static const generation_info_t GENERATIONS[] = {
    {
        .title = "generation-i",
        .range_start = 1,
        .range_end = 151,
        .versions = {
            {
                .name = "red-blue",
                .variants = {"back", "gray", "transparent", "back-gray"},
                .variant_count = 4
            },
            {
                .name = "yellow",
                .variants = {"back", "gbc", "gray", "transparent", "back-gbc", "back-gray", "back-transparent"},
                .variant_count = 7
            }
        },
        .version_count = 2
    },
    {
        .title = "generation-ii",
        .range_start = 152,
        .range_end = 251,
        .versions = {
            {
                .name = "gold",
                .variants = {"back", "shiny", "transparent", "back-shiny"},
                .variant_count = 4
            },
            {
                .name = "silver",
                .variants = {"back", "shiny", "transparent", "back-shiny"},
                .variant_count = 4
            },
            {
                .name = "crystal",
                .variants = {"back", "shiny", "back-shiny", "transparent", "back-transparent", "back-transparent-shiny"},
                .variant_count = 7
            }
        },
        .version_count = 3
    }
};

static const int GENERATION_COUNT = sizeof(GENERATIONS) / sizeof(GENERATIONS[0]);

static const char* DEFAULT_VERSIONS[] = {
    "red-blue",           // Gen 1
    "silver",            // Gen 2
    "ruby-sapphire",     // Gen 3
    "diamond-pearl",     // Gen 4
    "black-white",       // Gen 5
    "x-y",              // Gen 6
    "ultra-sun-ultra-moon", // Gen 7
    "icons"             // Gen 8
};

// Function declarations
Pokemon* pokemon_create(void);
void pokemon_free(Pokemon* pokemon);
bool pokemon_parse_json(const char* json_str, Pokemon* pokemon);
bool pokemon_build_sprite_url(char* url_buffer, size_t buffer_size, int pokedex, 
                            int generation, const char* version, const char* variant);
bool is_valid_generation(int generation);
bool is_valid_pokedex(int generation, int pokedex);
bool is_valid_version(int generation, const char* version);
const char* get_default_version(int generation);


#endif // POKEMON_H