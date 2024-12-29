#include<SoftwareSerial.h>
const int sensorPin = A0;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:
  int sensorValue = analogRead(sensorPin); // Read the analog sensor value

  // Convert the analog value to millimeters of rainfall (you may need to adjust this conversion)
  float rainfallInMM = map(sensorValue, 0, 1023, 0, 500);

  // Print the rainfall data in the desired format
  Serial.println(rainfallInMM, 7); // 7 decimal places for precision

  delay(1000);

}
