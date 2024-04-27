#include <ESP8266WiFi.h>
#include <SoftwareSerial.h>
#include <ESPDateTime.h>
#include "config.h"

const char* ssid = STASSID;
const char* password = STAPSK;

void setupWiFi() {
  Serial.begin(9600);
  DateTime.begin();

  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}