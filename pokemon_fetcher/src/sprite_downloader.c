// #include "../include/sprite_downloader.h"
// #include <string.h>
// #include <stdio.h>

// static size_t write_file_callback(void *ptr, size_t size, size_t nmemb, void *stream) {
//     return fwrite(ptr, size, nmemb, (FILE *)stream);
// }

// bool sprite_downloader_init(sprite_downloader_t* downloader) {
//     if (downloader == NULL) {
//         return false;
//     }

//     downloader->curl = curl_easy_init();
//     if (downloader->curl == NULL) {
//         return false;
//     }

//     downloader->error_buffer[0] = '\0';
//     return true;
// }

// void sprite_downloader_cleanup(sprite_downloader_t* downloader) {
//     if (downloader != NULL && downloader->curl != NULL) {
//         curl_easy_cleanup(downloader->curl);
//         downloader->curl = NULL;
//     }
// }

// bool sprite_build_url(char* url_buffer, size_t buffer_size, int pokedex, 
//                      int generation, const char* version, const char* variant) {
//     if (!url_buffer || buffer_size == 0) {
//         return false;
//     }

//     const char* base_url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/";
    
//     if (!is_valid_generation(generation)) {
//         return false;
//     }

//     const generation_info_t* gen = &GENERATIONS[generation - 1];
//     const char* ver = version ? version : get_default_version(generation);

//     if (!ver) {
//         return false;
//     }

//     // Build the URL
//     if (variant && is_valid_variant(generation, ver, variant)) {
//         snprintf(url_buffer, buffer_size, "%sversions/%s/%s/%s/%d.png",
//                 base_url, gen->title, ver, variant, pokedex);
//     } else {
//         snprintf(url_buffer, buffer_size, "%sversions/%s/%s/%d.png",
//                 base_url, gen->title, ver, pokedex);
//     }

//     return true;
// }

// bool sprite_download(sprite_downloader_t* downloader, const char* url, const char* output_path) {
//     if (!downloader || !downloader->curl || !url || !output_path) {
//         return false;
//     }

//     FILE* fp = fopen(output_path, "wb");
//     if (!fp) {
//         snprintf(downloader->error_buffer, CURL_ERROR_SIZE, "Failed to open file for writing: %s", output_path);
//         return false;
//     }

//     // Reset all options
//     curl_easy_reset(downloader->curl);

//     // Set up new options for file download
//     curl_easy_setopt(downloader->curl, CURLOPT_URL, url);
//     curl_easy_setopt(downloader->curl, CURLOPT_WRITEFUNCTION, write_file_callback);
//     curl_easy_setopt(downloader->curl, CURLOPT_WRITEDATA, fp);
//     curl_easy_setopt(downloader->curl, CURLOPT_FOLLOWLOCATION, 1L);
//     curl_easy_setopt(downloader->curl, CURLOPT_ERRORBUFFER, downloader->error_buffer);
    
//     // Add a user agent header
//     struct curl_slist* headers = curl_slist_append(NULL, 
//         "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36");
//     curl_easy_setopt(downloader->curl, CURLOPT_HTTPHEADER, headers);

//     // Perform the request
//     CURLcode res = curl_easy_perform(downloader->curl);
    
//     // Cleanup
//     curl_slist_free_all(headers);
//     fclose(fp);

//     if (res != CURLE_OK) {
//         remove(output_path);  // Delete partial file on error
//         return false;
//     }

//     // Check HTTP response code
//     long http_code = 0;
//     curl_easy_getinfo(downloader->curl, CURLINFO_RESPONSE_CODE, &http_code);
//     if (http_code != 200) {
//         remove(output_path);  // Delete file if HTTP error
//         snprintf(downloader->error_buffer, CURL_ERROR_SIZE, "HTTP error: %ld", http_code);
//         return false;
//     }

//     return true;
// }

// const char* sprite_get_error(const sprite_downloader_t* downloader) {
//     return downloader ? downloader->error_buffer : "Invalid downloader";
// }