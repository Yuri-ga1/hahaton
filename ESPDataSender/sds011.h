#include <SoftwareSerial.h>
#include "config.h"

SoftwareSerial sds(SDS_RX, SDS_TX);

struct SDS011Data {
  int pm25int;
  int pm10int;
};

SDS011Data readSDS011Data() {
  SDS011Data data;
  while (sds.available() && sds.read() != 0xAA) { }
  if (sds.available()) {
    byte buffer[10];
    buffer[0] = 0xAA;
    if (sds.available() >= 9) {
      sds.readBytes(&buffer[1], 9);
      if (buffer[9] == 0xAB) {
        data.pm25int = (buffer[3] << 8) | buffer[2];
        data.pm10int = (buffer[5] << 8) | buffer[4];
      } else {
        Serial.println("Invalid ending byte from SDS011.");
      }
    }
  }
  delay(1000);
  return data;
}


