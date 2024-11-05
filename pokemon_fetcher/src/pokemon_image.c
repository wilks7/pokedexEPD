#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <cairo.h>
#include <cairo-ft.h>
#include <curl/curl.h>
#include <png.h>
#include <ft2build.h>
#include FT_FREETYPE_H

#include "pokemon_image.h"
#include "pokemon.h"

// Structure to hold image data downloaded from the network
struct MemoryStruct {
    unsigned char *memory;
    size_t size;
};

// Callback function for libcurl to write data
static size_t WriteMemoryCallback(void *contents, size_t size, size_t nmemb, void *userp) {
    size_t realsize = size * nmemb;
    struct MemoryStruct *mem = (struct MemoryStruct *)userp;

    unsigned char *ptr = realloc(mem->memory, mem->size + realsize);
    if (!ptr) {
        // Out of memory
        fprintf(stderr, "Not enough memory (realloc returned NULL)\n");
        return 0;
    }

    mem->memory = ptr;
    memcpy(&(mem->memory[mem->size]), contents, realsize);
    mem->size += realsize;

    return realsize;
}

// Function to download image data from a URL
static unsigned char *download_image(const char *url, size_t *out_size) {
    CURL *curl_handle;
    CURLcode res;

    struct MemoryStruct chunk;
    chunk.memory = malloc(1); // Will be grown as needed by realloc
    chunk.size = 0;           // No data at this point

    curl_global_init(CURL_GLOBAL_ALL);
    curl_handle = curl_easy_init();

    if (!curl_handle) {
        fprintf(stderr, "Failed to initialize curl\n");
        free(chunk.memory);
        return NULL;
    }

    curl_easy_setopt(curl_handle, CURLOPT_URL, url);
    curl_easy_setopt(curl_handle, CURLOPT_WRITEFUNCTION, WriteMemoryCallback);
    curl_easy_setopt(curl_handle, CURLOPT_WRITEDATA, (void *)&chunk);

    // Follow redirects
    curl_easy_setopt(curl_handle, CURLOPT_FOLLOWLOCATION, 1L);

    // Perform the request
    res = curl_easy_perform(curl_handle);

    if (res != CURLE_OK) {
        fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
        free(chunk.memory);
        curl_easy_cleanup(curl_handle);
        curl_global_cleanup();
        return NULL;
    }

    curl_easy_cleanup(curl_handle);
    curl_global_cleanup();

    *out_size = chunk.size;
    return chunk.memory;
}

// Structure for reading PNG data from memory
typedef struct {
    const unsigned char *data;
    size_t size;
    size_t offset;
} png_memory_read_t;

// Cairo read function for PNG data
cairo_status_t cairo_read_func(void *closure, unsigned char *data, unsigned int length) {
    png_memory_read_t *png_data = (png_memory_read_t *)closure;

    if (png_data->offset + length > png_data->size) {
        length = png_data->size - png_data->offset;
    }

    memcpy(data, png_data->data + png_data->offset, length);
    png_data->offset += length;

    return CAIRO_STATUS_SUCCESS;
}

// Load PNG image from memory into a Cairo surface
cairo_surface_t* load_png_from_memory(const unsigned char *data, size_t size) {
    png_memory_read_t png_data = { data, size, 0 };
    cairo_surface_t *surface = cairo_image_surface_create_from_png_stream(cairo_read_func, &png_data);
    if (cairo_surface_status(surface) != CAIRO_STATUS_SUCCESS) {
        fprintf(stderr, "Failed to create image surface from PNG data: %s\n",
                cairo_status_to_string(cairo_surface_status(surface)));
        return NULL;
    }
    return surface;
}

// Convert hectograms to pounds (weight)
const char* kg_to_lb(int weight_hg) {
    static char buffer[32];
    double weight_kg = weight_hg / 10.0;
    double weight_lb = weight_kg * 2.20462;
    snprintf(buffer, sizeof(buffer), "%.1f lb", weight_lb);
    return buffer;
}

// Convert decimeters to feet and inches (height)
const char* meters_to_feet_inches(int height_dm) {
    static char buffer[32];
    double height_m = height_dm / 10.0;
    double total_inches = height_m * 39.3701;
    int feet = (int)(total_inches / 12);
    int inches = (int)(total_inches) % 12;
    snprintf(buffer, sizeof(buffer), "%d' %02d\"", feet, inches);
    return buffer;
}

// Wrap text into lines that fit within the specified width
char** wrap_text(cairo_t *cr, const char* text, double max_width) {
    // Split the text into words
    char* text_copy = strdup(text);
    if (!text_copy) {
        return NULL;
    }
    char* token = strtok(text_copy, " ");
    size_t lines_alloc = 10;
    char** lines = malloc(lines_alloc * sizeof(char*));
    if (!lines) {
        free(text_copy);
        return NULL;
    }
    size_t line_count = 0;
    char* line = calloc(1, strlen(text) + 1);
    if (!line) {
        free(text_copy);
        free(lines);
        return NULL;
    }
    line[0] = '\0';

    while (token != NULL) {
        char* temp_line;
        if (strlen(line) == 0) {
            temp_line = strdup(token);
        } else {
            temp_line = malloc(strlen(line) + strlen(token) + 2);
            if (!temp_line) {
                free(line);
                free(text_copy);
                for (size_t i = 0; i < line_count; i++) {
                    free(lines[i]);
                }
                free(lines);
                return NULL;
            }
            sprintf(temp_line, "%s %s", line, token);
        }

        cairo_text_extents_t extents;
        cairo_text_extents(cr, temp_line, &extents);
        if (extents.width > max_width) {
            // Save the current line
            lines[line_count++] = line;
            if (line_count >= lines_alloc) {
                lines_alloc *= 2;
                char** temp_lines = realloc(lines, lines_alloc * sizeof(char*));
                if (!temp_lines) {
                    free(temp_line);
                    free(text_copy);
                    for (size_t i = 0; i < line_count; i++) {
                        free(lines[i]);
                    }
                    free(lines);
                    return NULL;
                }
                lines = temp_lines;
            }
            // Start a new line
            line = strdup(token);
            free(temp_line);
        } else {
            free(line);
            line = temp_line;
        }
        token = strtok(NULL, " ");
    }

    // Add the last line
    lines[line_count++] = line;
    lines[line_count] = NULL; // Null-terminate the array

    free(text_copy);

    return lines;
}

// Draw the Pokémon sprite onto the canvas
// Draw the Pokémon sprite onto the canvas
int draw_pokemon_sprite(cairo_t *cr, const Pokemon* pokemon, int width, int height, double padding) {
    // Download the sprite image
    size_t image_data_size = 0;
    unsigned char *image_data = download_image(pokemon->sprite_url, &image_data_size);
    if (!image_data) {
        fprintf(stderr, "Failed to download image from %s\n", pokemon->sprite_url);
        return 0;
    }

    // Load the sprite into a Cairo surface
    cairo_surface_t *sprite_surface = load_png_from_memory(image_data, image_data_size);
    free(image_data); // Free the downloaded image data
    if (!sprite_surface) {
        fprintf(stderr, "Failed to load sprite image into Cairo surface\n");
        return 0;
    }

    // Get sprite dimensions
    int sprite_width = cairo_image_surface_get_width(sprite_surface);
    int sprite_height = cairo_image_surface_get_height(sprite_surface);

    // Define the image block dimensions
    double image_block_width = width / 2.0 - 2 * padding;  // Subtract padding
    double image_block_height = height / 2.0 - 2 * padding; // Subtract padding

    // Calculate scaling factors to fit the sprite into the image block
    double scale_x = image_block_width / sprite_width;
    double scale_y = image_block_height / sprite_height;

    // Use the smaller scaling factor to preserve aspect ratio
    double scale = (scale_x < scale_y) ? scale_x : scale_y;

    // Calculate new sprite dimensions after scaling
    double new_sprite_width = sprite_width * scale;
    double new_sprite_height = sprite_height * scale;

    // Calculate position to center the image within image_block
    double x = padding + (image_block_width - new_sprite_width) / 2.0;
    double y = padding + (image_block_height - new_sprite_height) / 2.0;

    // Draw the scaled sprite onto the canvas
    cairo_save(cr);
    cairo_translate(cr, x, y);
    cairo_scale(cr, scale, scale);
    cairo_set_source_surface(cr, sprite_surface, 0, 0);

    // Apply nearest-neighbor filtering for a pixelated look (optional)
    cairo_pattern_t *pattern = cairo_get_source(cr);
    cairo_pattern_set_filter(pattern, CAIRO_FILTER_NEAREST);

    cairo_paint(cr);
    cairo_restore(cr);

    cairo_surface_destroy(sprite_surface);

    return 1;
}

// Add Pokémon stats (name, species, weight, height) to the canvas
int add_pokemon_stats(cairo_t *cr, const Pokemon* pokemon, int width, int height, double padding) {
    // Initialize FreeType library
    FT_Library ft_library;
    if (FT_Init_FreeType(&ft_library)) {
        fprintf(stderr, "Could not init FreeType Library\n");
        return 0;
    }

    // Load the font face
    FT_Face ft_face;
    const char* font_path = "./fonts/pokemon_generation_1.ttf";
    if (FT_New_Face(ft_library, font_path, 0, &ft_face)) {
        fprintf(stderr, "Could not open font %s\n", font_path);
        FT_Done_FreeType(ft_library);
        return 0;
    }

    // Create a Cairo font face for use with Cairo
    cairo_font_face_t *cairo_ft_face = cairo_ft_font_face_create_for_ft_face(ft_face, 0);

    // Set font size
    double font_size = height / 16.0; // Adjust as needed
    if (font_size < 10) font_size = 10;

    cairo_set_font_face(cr, cairo_ft_face);
    cairo_set_font_size(cr, font_size);
    cairo_set_source_rgb(cr, 0, 0, 0); // Black color

    // Define the stats block dimensions
    double stats_block_x = width / 2.0;
    double stats_block_y = 0;
    double stats_block_width = width / 2.0;
    double stats_block_height = height / 2.0;

    // Starting positions
    double x = stats_block_x + padding;
    double y = stats_block_y + padding + font_size;

    // Draw Name
    cairo_move_to(cr, x, y);
    cairo_show_text(cr, pokemon->name);

    // Draw Species
    y += font_size + padding;
    cairo_move_to(cr, x, y);

    if (pokemon->type_count > 0 && pokemon->types[0] != NULL) {
        cairo_show_text(cr, pokemon->types[0]);
    } else {
        cairo_show_text(cr, "Unknown Type");
}

    // Draw Height
    y += font_size + padding;
    const char* height_text = meters_to_feet_inches(pokemon->height);
    char ht_label[64];
    snprintf(ht_label, sizeof(ht_label), "HT: %s", height_text);
    cairo_move_to(cr, x, y);
    cairo_show_text(cr, ht_label);

    // Draw Weight
    y += font_size + padding;
    const char* weight_text = kg_to_lb(pokemon->weight);
    char wt_label[64];
    snprintf(wt_label, sizeof(wt_label), "WT: %s", weight_text);
    cairo_move_to(cr, x, y);
    cairo_show_text(cr, wt_label);

    // Clean up
    cairo_font_face_destroy(cairo_ft_face);
    FT_Done_Face(ft_face);
    FT_Done_FreeType(ft_library);

    return 1;
}

double optimize_font_size(cairo_t *cr, const char* text, const char* font_path, double max_width, double max_height, double initial_font_size) {
    double font_size = initial_font_size;
    char** lines = NULL;

    while (1) {
        // Set font size
        cairo_set_font_size(cr, font_size);

        // Wrap text
        if (lines) {
            for (int i = 0; lines[i] != NULL; i++) {
                free(lines[i]);
            }
            free(lines);
        }
        lines = wrap_text(cr, text, max_width);
        if (!lines) {
            break;
        }

        // Calculate total text height
        cairo_text_extents_t extents;
        double line_spacing = font_size * 0.2; // 20% of font size
        double total_height = 0;
        for (int i = 0; lines[i] != NULL; i++) {
            cairo_text_extents(cr, lines[i], &extents);
            total_height += extents.height + line_spacing;
        }

        // Check if text exceeds the available height
        if (total_height > max_height) {
            font_size -= 1;
            break;
        }

        font_size += 1;
    }

    // Clean up
    if (lines) {
        for (int i = 0; lines[i] != NULL; i++) {
            free(lines[i]);
        }
        free(lines);
    }

    return font_size;
}


// Add Pokémon description to the canvas
int add_pokemon_description(cairo_t *cr, const Pokemon* pokemon, int width, int height, double padding) {
    // Initialize FreeType library
    FT_Library ft_library;
    if (FT_Init_FreeType(&ft_library)) {
        fprintf(stderr, "Could not init FreeType Library\n");
        return 0;
    }

    // Load the font face
    FT_Face ft_face;
    const char* font_path = "./fonts/pokemon_generation_1.ttf";
    if (FT_New_Face(ft_library, font_path, 0, &ft_face)) {
        fprintf(stderr, "Could not open font %s\n", font_path);
        FT_Done_FreeType(ft_library);
        return 0;
    }

    // Create a Cairo font face for use with Cairo
    cairo_font_face_t *cairo_ft_face = cairo_ft_font_face_create_for_ft_face(ft_face, 0);

    // Define the description area
    double desc_block_x = padding;
    double desc_block_y = height / 2.0 + padding;
    double desc_block_width = width - 2 * padding;
    double desc_block_height = height / 2.0 - 2 * padding;

    // Set font face
    cairo_set_font_face(cr, cairo_ft_face);

    // Optimize font size to fill the area
    double initial_font_size = 10; // Starting font size
    double font_size = optimize_font_size(cr, pokemon->description, font_path, desc_block_width, desc_block_height, initial_font_size);
    if (font_size < 8) font_size = 8;

    // Set optimized font size
    cairo_set_font_size(cr, font_size);
    cairo_set_source_rgb(cr, 0, 0, 0); // Black color

    // Wrap text with optimized font size
    char** lines = wrap_text(cr, pokemon->description, desc_block_width);
    if (!lines) {
        // Clean up
        cairo_font_face_destroy(cairo_ft_face);
        FT_Done_Face(ft_face);
        FT_Done_FreeType(ft_library);
        return 0;
    }

    // Draw lines
    double x = desc_block_x;
    double y = desc_block_y + font_size;
    double line_spacing = font_size * 0.2; // 20% of font size

    for (int i = 0; lines[i] != NULL; i++) {
        cairo_move_to(cr, x, y);
        cairo_show_text(cr, lines[i]);
        y += font_size + line_spacing;
        free(lines[i]); // Free each line
    }
    free(lines); // Free the array

    // Clean up
    cairo_font_face_destroy(cairo_ft_face);
    FT_Done_Face(ft_face);
    FT_Done_FreeType(ft_library);

    return 1;
}

// Draw a custom line with square patterns across the canvas
void draw_custom_line(cairo_t *cr, int width, int height) {
    // Parameters
    double thickness = 8.0;
    int num_squares = 4;
    double square_size = 2.4 * thickness;
    double square_thickness = thickness / 1.4;
    double padding = 20.0; // Adjust as needed

    // Y-coordinate of the midway point
    double y_mid = height / 2.0;

    // Draw the horizontal line across the entire width
    cairo_set_source_rgb(cr, 0, 0, 0); // Black color
    cairo_set_line_width(cr, thickness);
    cairo_move_to(cr, 0, y_mid);
    cairo_line_to(cr, width, y_mid);
    cairo_stroke(cr);

    // Calculate total available width for squares and gaps on each side
    double available_width = (width / 2.0) - padding;

    // Calculate total width needed for squares and gaps
    double num_gaps = num_squares + 1;
    double total_squares_width = num_squares * square_size;
    double gap_size = (available_width - total_squares_width) / num_gaps;

    if (gap_size < 0) {
        fprintf(stderr, "Not enough space to draw squares with the given parameters.\n");
        return;
    }

    // Left side squares (from center towards left)
    for (int i = 0; i < num_squares; i++) {
        double x_left = (width / 2.0) - padding - gap_size - square_size - i * (square_size + gap_size);
        cairo_rectangle(cr, x_left, y_mid - square_size / 2.0, square_size, square_size);
        
        // Draw the square
        cairo_set_source_rgb(cr, 1, 1, 1); // White fill
        cairo_fill_preserve(cr);
        cairo_set_source_rgb(cr, 0, 0, 0); // Black outline
        cairo_set_line_width(cr, square_thickness);
        cairo_stroke(cr);
    }

    // Right side squares (from center towards right)
    for (int i = 0; i < num_squares; i++) {
        double x_right = (width / 2.0) + padding + gap_size + i * (square_size + gap_size);
        cairo_rectangle(cr, x_right, y_mid - square_size / 2.0, square_size, square_size);
        
        // Draw the square
        cairo_set_source_rgb(cr, 1, 1, 1); // White fill
        cairo_fill_preserve(cr);
        cairo_set_source_rgb(cr, 0, 0, 0); // Black outline
        cairo_set_line_width(cr, square_thickness);
        cairo_stroke(cr);
    }
}

// Create the Pokedex image with the specified resolution
int create_pokedex_image(const char* filename, const Pokemon* pokemon, int width, int height) {
    // Ensure width and height are positive integers
    if (width <= 0 || height <= 0) {
        fprintf(stderr, "Invalid image dimensions: %dx%d\n", width, height);
        return 0;
    }

    // Initialize Cairo surface and context
    cairo_surface_t *surface = cairo_image_surface_create(CAIRO_FORMAT_RGB24, width, height);
    if (cairo_surface_status(surface) != CAIRO_STATUS_SUCCESS) {
        fprintf(stderr, "Failed to create Cairo surface: %s\n",
                cairo_status_to_string(cairo_surface_status(surface)));
        return 0;
    }
    cairo_t *cr = cairo_create(surface);
    if (cairo_status(cr) != CAIRO_STATUS_SUCCESS) {
        fprintf(stderr, "Failed to create Cairo context: %s\n",
                cairo_status_to_string(cairo_status(cr)));
        cairo_surface_destroy(surface);
        return 0;
    }

    // Set background color (white)
    cairo_set_source_rgb(cr, 1.0, 1.0, 1.0);
    cairo_paint(cr);

    // Define padding and other layout parameters
    double padding = height * 0.05;

    // Draw the Pokémon sprite image
    if (!draw_pokemon_sprite(cr, pokemon, width, height, padding)) {
        fprintf(stderr, "Failed to draw Pokémon sprite\n");
        cairo_destroy(cr);
        cairo_surface_destroy(surface);
        return 0;
    }

    // Add stats (name, species, weight, height)
    if (!add_pokemon_stats(cr, pokemon, width, height, padding)) {
        fprintf(stderr, "Failed to add Pokémon stats\n");
        cairo_destroy(cr);
        cairo_surface_destroy(surface);
        return 0;
    }

    // Add description
    if (!add_pokemon_description(cr, pokemon, width, height, padding)) {
        fprintf(stderr, "Failed to add Pokémon description\n");
        cairo_destroy(cr);
        cairo_surface_destroy(surface);
        return 0;
    }

    // Draw custom line with square patterns
    draw_custom_line(cr, width, height);

    // Save the image to a file
    cairo_status_t status = cairo_surface_write_to_png(surface, filename);
    if (status != CAIRO_STATUS_SUCCESS) {
        fprintf(stderr, "Failed to write image to file %s: %s\n", filename,
                cairo_status_to_string(status));
        cairo_destroy(cr);
        cairo_surface_destroy(surface);
        return 0;
    }

    // Clean up
    cairo_destroy(cr);
    cairo_surface_destroy(surface);

    return 1;
}
