#ifndef API_MANAGER_H
#define API_MANAGER_H

#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <ArduinoJson.h>

#define JSON_SIZE 1024

class APIManager {
  private:
    const char* ssid;        ///< SSID du réseau WiFi
    const char* password;    ///< Mot de passe du réseau WiFi
    String serverUrl;        ///< URL de l'API cible

  public:
    APIManager(const char* ssid, const char* password, const String& serverUrl);
    void begin();
    bool getData(const String& api_path = "/");
    void sendData(const StaticJsonDocument<JSON_SIZE>& jsonDoc, const String& api_path, const String& method = "POST");
    // APIManager(const char* ssid, const char* password, const String& serverUrl) 
    //   : ssid(ssid), password(password), serverUrl(serverUrl) {}

    // void begin() {
    //   // Connexion au réseau WiFi
    //   Serial.println("Connecting to WiFi...");
    //   WiFi.begin(ssid, password);
    //   while (WiFi.status() != WL_CONNECTED) {
    //     delay(500);
    //     Serial.print(".");
    //   }
    //   Serial.println("\nConnected to WiFi.");
    //   Serial.print("IP Address: ");
    //   Serial.println(WiFi.localIP());
    // }
    // bool getData(const String& api_path = "/") {
    //   if (WiFi.status() == WL_CONNECTED) {
    //     WiFiClient client;
    //     HTTPClient http;

    //     // Initialise la connexion HTTP
    //     http.begin(client, serverUrl + api_path);

    //     // Envoyer la requête HTTP GET
    //     int httpResponseCode = http.GET();

    //     if (httpResponseCode == 200) {
    //       // Le serveur est en bonne santé
    //       http.end();
    //       return true;
    //     } else {
    //       // Le serveur n'est pas en bonne santé
    //       http.end();
    //       return false;
    //     }
    //   } else {
    //     Serial.println("WiFi disconnected!");
    //     return false;
    //   }
    // }
    // void sendData(const StaticJsonDocument<JSON_SIZE>& jsonDoc, const String& api_path, const String& method = "POST") {
    //   // Vérifie si le WiFi est connecté
    //   if (WiFi.status() == WL_CONNECTED) {
    //     WiFiClient client;
    //     HTTPClient http;

    //     // Initialise la connexion HTTP
    //     http.begin(client, serverUrl + api_path);
    //     http.addHeader("Content-Type", "application/json");

    //     String jsonString;
    //     serializeJson(jsonDoc, jsonString);

    //     // Envoyer la requête HTTP POST
    //     int httpResponseCode = -1;
    //     if(method == "POST")
    //       httpResponseCode = http.POST(jsonString);

    //     if (httpResponseCode > 0) {
    //       // Affiche le code de réponse HTTP et la réponse
    //       Serial.print("HTTP Response code: ");
    //       Serial.println(httpResponseCode);
    //       String payload = http.getString();
    //       Serial.println("Response: " + payload);
    //     } else {
    //       Serial.print("Error code: ");
    //       Serial.println(httpResponseCode);
    //     }

    //     // Libère les ressources
    //     http.end();
    //   } else {
    //     Serial.println("WiFi disconnected!");
    //   }
    // }

};

#endif
