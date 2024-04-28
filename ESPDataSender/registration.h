#include <ArduinoJson.h>
#include <ESP8266HTTPClient.h>
#include "config.h"

void sendRegistrationRequest() {
  DynamicJsonDocument regDoc(2048);
  regDoc["mac"] = WiFi.macAddress();
  String regJson;
  serializeJson(regDoc, regJson);
  // Serial.println(regDoc);
  Serial.print("regJson: ");
  Serial.println(regJson);
  String regUrl = "http://"+String(URL) + "/registerDevice";
  Serial.println(regUrl);
  HTTPClient regHttp;
  WiFiClient regClient;
  regHttp.begin(regClient, regUrl);
  regHttp.addHeader("Content-Type", "application/json");

  int regHttpCode = regHttp.POST(regJson);
  Serial.println(regHttpCode);
  while (regHttpCode != 200){
    int regHttpCode = regHttp.POST(regJson);
  }
  if (regHttpCode > 0) {
    String regPayload = regHttp.getString();
    Serial.println(regPayload);
  } else {
    Serial.println("Error sending registration request");
  }
}
