#include<SoftwareSerial.h>
#include <ArduinoJson.h>
const int rainSensorPin = A0;
SoftwareSerial mySerial(6,7);
void setup() {
  Serial.begin(9600);
  mySerial.begin(4800);
  Serial.begin(9600);

}
void loop(){
  int sensorValue = analogRead(rainSensorPin); 
  byte queryData[] {0x01,0x03,0x00,0x00,0x00,0x07,0x04,0x08};
  byte receivedData[19];
  mySerial.write(queryData, sizeof(queryData));
  delay(5000);
  if(mySerial.available() >= sizeof(receivedData)){
    mySerial.readBytes(receivedData, sizeof(receivedData));
    unsigned int soilHumidity = (receivedData[3]<<8) | receivedData[4];
    unsigned int soilTemperature = (receivedData[5]<<8) | receivedData[6];
    unsigned int soilConductivity = (receivedData[7]<<8) | receivedData[8];
    unsigned int soilPH = (receivedData[9]<<8) | receivedData[10];
    unsigned int nitrogen = (receivedData[11]<<8) | receivedData[12];
    unsigned int phosphorus = (receivedData[13]<<8) | receivedData[14];
    unsigned int potassium = (receivedData[15]<<8) | receivedData[16];
    Serial.println(data);
  }
  delay(500);
}