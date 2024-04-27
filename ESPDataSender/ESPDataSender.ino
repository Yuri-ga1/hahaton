#include <Arduino.h>
#include "wifi.h"
#include "registration.h"
#include "sds011.h"



void setup() {
  setupWiFi();

  sds.begin(9600);
  sendRegistrationRequest();
}

void loop() {
  sendData();
}

void sendData(){
  SDS011Data data = readSDS011Data();
  if (data.pm25int != 0 && data.pm10int != 0) {
    float pm2_5 = data.pm25int / 10.0;
    float pm10 = data.pm10int / 10.0;

    DynamicJsonDocument doc(2048);
    doc["mac"] = WiFi.macAddress();
    doc["date"] = DateTime.now();
    doc["pm2_5"] = pm2_5;
    doc["pm10"] = pm10;

    String jsonStr;
    serializeJson(doc, jsonStr);
    Serial.print(jsonStr);
    sendDataOnServer(jsonStr);
    }
}

void sendDataOnServer(String jsonStr) {
  HTTPClient http;
  WiFiClient client;
  String serverUrl = "http://"+String(URL)+"/dataReceiver";	
  http.begin(client, serverUrl);
  http.addHeader("Content-Type", "application/json");
  Serial.println(serverUrl);
  int httpCode = http.POST(jsonStr);

  if (httpCode > 0) {
    String payload = http.getString();
    Serial.println(payload);
  } else {
    Serial.println("Error sending POST request");
  }
}