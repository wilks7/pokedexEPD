#include "pokemon.h"
#include <string.h>
#include <stdio.h>

// Helper function to extract string value between quotes
static char* extract_string(const char* json, const char* key) {
    char search_key[256];
    snprintf(search_key, sizeof(search_key), "\"%s\":\"", key);
    
    const char* start = strstr(json, search_key);
    if (!start) return NULL;
    
    start += strlen(search_key);
    const char* end = strchr(start, '"');
    if (!end) return NULL;
    
    size_t len = end - start;
    char* result = malloc(len + 1);
    if (!result) return NULL;
    
    strncpy(result, start, len);
    result[len] = '\0';
    return result;
}

// Helper function to extract integer value
static int extract_int(const char* json, const char* key, int default_value) {
    char search_key[256];
    snprintf(search_key, sizeof(search_key), "\"%s\":", key);
    
    const char* start = strstr(json, search_key);
    if (!start) return default_value;
    
    start += strlen(search_key);
    while (*start == ' ' || *start == '\t' || *start == '\n' || *start == '\r') start++;
    
    return atoi(start);
}

// Helper function to extract array of types
static void extract_types(const char* json, Pokemon* pokemon) {
    const char* types_start = strstr(json, "\"types\":[");
    if (!types_start) return;
    
    const char* name_ptr = types_start;
    pokemon->type_count = 0;
    while ((name_ptr = strstr(name_ptr + 1, "\"name\":"))) {
        pokemon->type_count++;
    }
    
    if (pokemon->type_count == 0) return;
    
    pokemon->types = calloc(pokemon->type_count, sizeof(char*));
    if (!pokemon->types) {
        pokemon->type_count = 0;
        return;
    }
    
    const char* current = types_start;
    for (int i = 0; i < pokemon->type_count; i++) {
        current = strstr(current + 1, "\"name\":\"");
        if (!current) break;
        
        current += strlen("\"name\":\"");
        const char* end = strchr(current, '"');
        if (!end) break;
        
        size_t len = end - current;
        pokemon->types[i] = malloc(len + 1);
        if (pokemon->types[i]) {
            strncpy(pokemon->types[i], current, len);
            pokemon->types[i][len] = '\0';
        }
    }
}

// Helper function to extract flavor text (description)
static char* extract_flavor_text(const char* json) {
    const char* flavor_texts_start = strstr(json, "\"flavorTexts\":[");
    if (!flavor_texts_start) return NULL;

    const char* flavor_start = strstr(flavor_texts_start, "\"flavor\":\"");
    if (!flavor_start) return NULL;

    flavor_start += strlen("\"flavor\":\"");

    // Find the end of the flavor text
    const char* flavor_end = flavor_start;
    while (*flavor_end && *flavor_end != '"') {
        // Handle escaped quotes
        if (*flavor_end == '\\' && *(flavor_end + 1) == '"') {
            flavor_end += 2;
        } else {
            flavor_end++;
        }
    }

    size_t len = flavor_end - flavor_start;
    char* result = malloc(len + 1);
    if (!result) return NULL;

    // Copy the flavor text, handling escaped quotes
    char* dest = result;
    const char* src = flavor_start;
    while (src < flavor_end) {
        if (*src == '\\' && *(src + 1) == '"') {
            *dest++ = '"';
            src += 2;
        } else if (*src == '\\' && *(src + 1) == 'n') {
            *dest++ = ' ';
            src += 2;
        } else if (*src == '\n' || *src == '\r') {
            // Replace newlines with spaces
            *dest++ = ' ';
            src++;
        } else {
            *dest++ = *src++;
        }
    }
    *dest = '\0';

    return result;
}

// Pokemon creation and management
Pokemon* pokemon_create(void) {
    Pokemon* pokemon = calloc(1, sizeof(Pokemon));
    if (pokemon) {
        pokemon->name = NULL;
        pokemon->sprite_url = NULL;
        pokemon->types = NULL;
        pokemon->type_count = 0;
    }
    return pokemon;
}

void pokemon_free(Pokemon* pokemon) {
    if (pokemon) {
        free(pokemon->name);
        free(pokemon->sprite_url);
        
        if (pokemon->types) {
            for (int i = 0; i < pokemon->type_count; i++) {
                free(pokemon->types[i]);
            }
            free(pokemon->types);
        }
        
        free(pokemon);
    }
}

// JSON parsing
bool pokemon_parse_json(const char* json_str, Pokemon* pokemon) {
    if (!json_str || !pokemon) return false;

    const char* data_start = strstr(json_str, "\"getPokemonByDexNumber\":{");
    if (!data_start) return false;

    pokemon->name = extract_string(data_start, "species");
    if (!pokemon->name) return false;

    pokemon->id = extract_int(data_start, "num", 0);
    pokemon->height = extract_int(data_start, "height", 0);
    pokemon->weight = extract_int(data_start, "weight", 0);

    extract_types(data_start, pokemon);

    // Extract the description (flavor text)
    pokemon->description = extract_flavor_text(data_start);
    if (!pokemon->description) {
        // Provide a default description if none is found
        pokemon->description = strdup("No description available.");
    }

    return true;
}

// Sprite and generation handling
bool is_valid_generation(int generation) {
    return (generation > 0 && generation <= GENERATION_COUNT);
}

bool is_valid_pokedex(int generation, int pokedex) {
    if (!is_valid_generation(generation)) return false;
    const generation_info_t* gen = &GENERATIONS[generation - 1];
    return (pokedex >= gen->range_start && pokedex <= gen->range_end);
}

const char* get_default_version(int generation) {
    if (!is_valid_generation(generation)) return NULL;
    return DEFAULT_VERSIONS[generation - 1];
}

bool pokemon_build_sprite_url(char* url_buffer, size_t buffer_size, int pokedex, 
                            int generation, const char* version, const char* variant) {
    if (!url_buffer || buffer_size == 0) {
        return false;
    }

    if (!is_valid_generation(generation)) {
        return false;
    }

    // Get the generation info
    const generation_info_t* gen = &GENERATIONS[generation - 1];
    
    // If no version specified, use default
    const char* ver = version;
    if (!ver) {
        ver = get_default_version(generation);
    }

    // Validate version exists for this generation
    bool version_valid = false;
    for (int i = 0; i < gen->version_count; i++) {
        if (strcmp(gen->versions[i].name, ver) == 0) {
            version_valid = true;
            break;
        }
    }

    if (!version_valid) {
        return false;
    }

    // Build the URL
    if (variant) {
        snprintf(url_buffer, buffer_size, "%s/versions/%s/%s/%s/%d.png",
                SPRITE_BASE_URL, gen->title, ver, variant, pokedex);
    } else {
        snprintf(url_buffer, buffer_size, "%s/versions/%s/%s/%d.png",
                SPRITE_BASE_URL, gen->title, ver, pokedex);
    }

    return true;
}

bool is_valid_version(int generation, const char* version) {
    if (!is_valid_generation(generation)) {
        return false;
    }

    const generation_info_t* gen = &GENERATIONS[generation - 1];
    
    for (int i = 0; i < gen->version_count; i++) {
        if (strcmp(gen->versions[i].name, version) == 0) {
            return true;
        }
    }
    
    return false;
}