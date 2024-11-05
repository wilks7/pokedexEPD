// #ifndef SPRITE_DOWNLOADER_H
// #define SPRITE_DOWNLOADER_H

// #include <curl/curl.h>
// #include <stdbool.h>
// #include "pokemon_constants.h"

// typedef struct {
//     CURL* curl;
//     char error_buffer[CURL_ERROR_SIZE];
// } sprite_downloader_t;

// // Initialize the sprite downloader
// bool sprite_downloader_init(sprite_downloader_t* downloader);

// // Cleanup the sprite downloader
// void sprite_downloader_cleanup(sprite_downloader_t* downloader);

// // Build sprite URL
// bool sprite_build_url(char* url_buffer, size_t buffer_size, int pokedex, 
//                      int generation, const char* version, const char* variant);

// // Download sprite image to a file
// bool sprite_download(sprite_downloader_t* downloader, const char* url, const char* output_path);

// // Get the last error message
// const char* sprite_get_error(const sprite_downloader_t* downloader);

// #endif // SPRITE_DOWNLOADER_H