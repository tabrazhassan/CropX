#include <WiFi.h>
#include <FirebaseArduino.h>
#define RXp2 16
#define TXp2 17
const char* ssid = "Hasan";
const char* password = "Mashouq123";
#define FIREBASE_HOST "https://cropx-7a72d-default-rtdb.firebaseio.com"
#define FIREBASE_AUTH "CF1SCyk1Kuiwz6ZCrZ07jBH4SMBSetcm6OvvjL7K"
FirebaseData firebaseData;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial2.begin(9600, SERIAL_8N1, RXp2, TXp2);
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to WiFi");
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  Firebase.reconnectWiFi(true);
}

void loop() {
  // put your main code here, to run repeatedly:
  String serialData =Serial2.readString();
  float sensorValue = serialData.toFloat();
  if (Firebase.setFloat(firebaseData, "/sensor/value", sensorValue)) {
    Serial.println("Data sent to Firebase successfully");
  } else {
    Serial.println("Error sending data to Firebase");
  }

  delay(5000);

}
