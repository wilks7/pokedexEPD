#ifndef NETWORK_H
#define NETWORK_H

#include <stdbool.h>
#include <curl/curl.h>

// Response structure for network requests
typedef struct {
    char* data;
    size_t size;
} Response;

// Initialize networking
bool network_init(void);

// Cleanup networking
void network_cleanup(void);

// Make a POST request
char* make_graphql_request(const char* url, const char* query);

#endif // NETWORK_H