#include "network.h"
#include <stdlib.h>
#include <string.h>

// Callback function for CURL
static size_t write_callback(void* contents, size_t size, size_t nmemb, void* userp) {
    size_t real_size = size * nmemb;
    Response* resp = (Response*)userp;

    char* ptr = realloc(resp->data, resp->size + real_size + 1);
    if (!ptr) {
        return 0;
    }

    resp->data = ptr;
    memcpy(&(resp->data[resp->size]), contents, real_size);
    resp->size += real_size;
    resp->data[resp->size] = 0;

    return real_size;
}

bool network_init(void) {
    return (curl_global_init(CURL_GLOBAL_DEFAULT) == CURLE_OK);
}

void network_cleanup(void) {
    curl_global_cleanup();
}

char* make_graphql_request(const char* url, const char* query) {
    CURL* curl = curl_easy_init();
    if (!curl) {
        return NULL;
    }

    // Set up response structure
    Response response = {
        .data = malloc(1),
        .size = 0
    };

    if (!response.data) {
        curl_easy_cleanup(curl);
        return NULL;
    }

    // Set up CURL
    struct curl_slist* headers = curl_slist_append(NULL, "Content-Type: application/json");
    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, query);
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void*)&response);

    // Perform request
    CURLcode res = curl_easy_perform(curl);
    curl_slist_free_all(headers);
    curl_easy_cleanup(curl);

    if (res != CURLE_OK) {
        free(response.data);
        return NULL;
    }

    return response.data;
}