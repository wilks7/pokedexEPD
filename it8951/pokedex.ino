#include <WiFi.h>
#include "config.h"
#include <HTTPClient.h>

const uint serverPort = 8319;
WiFiServer server(serverPort);
bool acceptMode = true; // Set this to false if you want "check" mode


void pinSetup() {
  pinMode(MISO, INPUT);
  pinMode(MOSI, OUTPUT);
  pinMode(SCK, OUTPUT);
  pinMode(CS, OUTPUT);
  pinMode(RESET, OUTPUT);
  pinMode(HRDY, INPUT);
}

void enterDeepSleep() {
  Serial.println("Entering deep sleep for 1 minute...");
  IT8951Sleep();
  esp_sleep_enable_timer_wakeup(60 * 1000000); // Sleep for 60 seconds (microseconds)
  esp_deep_sleep_start();
}

void setup(void) {
  pinSetup();

  Serial.begin(115200);
  while (!Serial) {}

  Serial.println("Trying to connect to Wifi SSID: ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  if (WiFi.waitForConnectResult() != WL_CONNECTED) {
    Serial.println("WiFi Connect Failed! Rebooting...");
    delay(1000);
    ESP.restart();
  }
  Serial.print("WiFi connected successfully. ");
  Serial.println(WiFi.localIP());

  if (IT8951_Init() != 0) {
    Serial.println("Display init failed");
    exit(1);
  };
  Serial.println("Display init successful");
  Serial.println(WiFi.localIP());

  uint32_t batteryVoltage = getBatteryVoltage();
  Serial.printf("Battery Voltage: %.2f V\n", batteryVoltage / 1000.0); // Convert to volts for display

    // Calculate and Print Battery Percentage
  int batteryPercentage = calculateBatteryPercentage(batteryVoltage / 1000.0); // Convert to volts
  Serial.printf("Battery Percentage: %d%%\n", batteryPercentage);

  if (acceptMode) {
    Serial.println("Starting in Accept Mode");
    server.begin();
  } else {
    Serial.println("Starting in Check Mode");
    fetchCommandData();
    enterDeepSleep(); // Enter deep sleep after fetching the command
  }
}

void loop() {
  // Check for new client commands
  if (acceptMode) {
    WiFiClient client = server.available();
    if (client) {
      while (client.connected()) {
        while (client.available() > 0) {
          CommandHeader header;
          int size = client.read((uint8_t *)&header, sizeof(CommandHeader));
          Serial.print("Data Read: ");
          Serial.println(size);
          if (size == sizeof(CommandHeader)) {
            Serial.print("Command: ");
            Serial.println(header.command);
            handleClientCommand(client, header);
          }
        }
        delay(10);
      }

      client.stop();
      Serial.println("Client disconnected");
      // IT8951Sleep();
    }
  }
}

  // Fetch image data every 20 seconds for testing
//   static unsigned long lastFetchTime = 0;
//   if (millis() - lastFetchTime > 20000) { 
//     // fetchImageData();
//     fetchCommandData();
//     lastFetchTime = millis();
//   }
// }
