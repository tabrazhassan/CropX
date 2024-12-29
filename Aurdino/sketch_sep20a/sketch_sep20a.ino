#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "DESKTOP-4VBBPEO 5427";
const char* password = "0123456788";
const char* sheetURL = "https://script.google.com/macros/s/AKfycbzTNLp-QGEstnevE9QGecEt6W4vpt6zSChw4vsE-k4nqCRr9iPeYKvuHjRQ49xkOa4z/exec"; // Replace with your web app URL

#define RXp2 16
#define TXp2 17

void setup() {
  Serial.begin(115200);
  Serial2.begin(9600, SERIAL_8N1, RXp2, TXp2);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  if (Serial2.available()) {
    String data = Serial2.readString();
    sendDataToGoogleSheet(data);
  }
}

void sendDataToGoogleSheet(String data) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(sheetURL);
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");

    String postData = "data=" + data; // Assuming 'data' is the parameter name expected by the Google Apps Script

    int httpResponseCode = http.POST(postData);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("HTTP Response Code: " + String(httpResponseCode));
      Serial.println("Response: " + response);
    } else {
      Serial.println("Error sending data to Google Sheet");
    }

    http.end();
  } else {
    Serial.println("Not connected to WiFi");
  }
}
