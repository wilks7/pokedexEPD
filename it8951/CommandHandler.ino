#include <WiFi.h>
#include <HTTPClient.h>

#define MAX_BATCH 1024

// Struct definition must be declared before use
typedef struct {
  uint8_t command;
  uint8_t color;
  uint16_t x, y;
  uint16_t w, h;
} CommandHeader;

// Forward declaration of the function to ensure the compiler recognizes it before it's called
void handleClientC(WiFiClient &client, CommandHeader &header);
void handleClientCommand(WiFiClient &client, CommandHeader &header);

void fetchCommandData() {
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("Attempting to connect to command server...");
    WiFiClient client;
    if (client.connect("10.0.0.87", 8319)) { // Replace with your Mac's IP and port
      Serial.println("Successfully connected to command server. Waiting for command...");

      // Wait for data to be available before attempting to read
      unsigned long startTime = millis();
      while (client.available() == 0 && millis() - startTime < 5000) {
        delay(100); // Wait for up to 5 seconds for data to become available
      }

      while (client.connected()) {
        if (client.available() > 0) {
          // Assume command structure received, read the header and pass it to handleClientC
          CommandHeader header;
          int bytesRead = client.read((uint8_t *)&header, sizeof(CommandHeader));

          if (bytesRead == sizeof(CommandHeader)) {
            handleClientCommand(client, header);
            Serial.println("Command processed successfully.");
          } else {
            Serial.println("Failed to read a complete command header.");
          }
        } else {
          delay(10);  // Short delay to prevent tight looping
        }
      }

      client.stop();
      Serial.println("Disconnected from command server.");
    } else {
      Serial.println("Failed to connect to command server.");
    }
  } else {
    Serial.println("WiFi not connected. Cannot fetch command.");
  }
}

void handleClientCommand(WiFiClient &client, CommandHeader &header) {
  Serial.print("Processing command: ");
  Serial.println(header.command);
  
  Serial.print("Color: ");
  Serial.println(header.color);

  if (header.command == 1) {
    Serial.println("Clearing screen...");
    IT8951LoadDataStart(header.x, header.y, header.w, header.h);
    uint8_t c = header.color & 0xf;
    c = (c << 4) | (header.color & 0xf);
    for (int j = 0; j < header.h; j++)
      for (int i = 0; i < header.w / 2; i++)
        IT8951LoadDataColor(c);
    IT8951LoadDataEnd();
    
    // Explicitly refresh the display area
    // IT8951DisplayArea(header.x, header.y, header.w, header.h, 2);
    Serial.println("Screen clearing.");
  } else if (header.command == 2) {
    IT8951LoadDataStart(header.x, header.y, header.w, header.h);
    int totalBytes = header.h * header.w / 2;
    while (totalBytes > 0) {
      int batchSize = totalBytes;
      if (batchSize > MAX_BATCH)
        batchSize = MAX_BATCH;
      if (batchSize > client.available())
        batchSize = client.available();

      if (batchSize == 0) {
        delay(2);
        continue;
      }
      uint8_t *c = new uint8_t[batchSize];
      int size = client.read(c, batchSize);
      if (size != -1) {
        IT8951LoadDataColor(c, size);
        free(c);
        totalBytes -= size;
      }
    }
    IT8951LoadDataEnd();
  } else if (header.command == 4) {
    Serial.println("Displaying Loaded Data...");
    IT8951DisplayArea(header.x, header.y, header.w, header.h, 2);
  } 
}