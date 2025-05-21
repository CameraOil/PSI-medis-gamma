#include <ModbusRtu.h>

// RX1 --> RO
// TX1 --> DI

#define TXEN 4                // DE and RE tied together to digital pin 4
#define PHOTODIODE A0
#define TGS822 A1

Modbus slave(1, Serial1, TXEN);  // ID = 1, use Serial1 (TX1/RX1)

uint16_t data[2];  // Register buffer

void setup() {
  pinMode(TXEN, OUTPUT);
  digitalWrite(TXEN, 0);       // Initially set to receive
  Serial1.begin(9600);         // Serial1 for RS485
  Serial.begin(9600);
  slave.start();
}

void loop() {
  data[0] = analogRead(PHOTODIODE);  // Light sensor
  // data[0] = 200;
  data[1] = analogRead(TGS822);      // Gas sensor
  // data[1] = 50;
  // Serial.println("sent");
  slave.poll(data, 2);               // Expose registers 0 and 1
}
