#include "API_Manager.h"

APIManager::APIManager(const char* ssid, const char* password, const String& serverUrl) 
      : ssid(ssid), password(password), serverUrl(serverUrl) {}

    void APIManager::begin() {
      // Connexion au réseau WiFi
      Serial.println("En train de connecter sur WiFi...");
      WiFi.begin(ssid, password);
      while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
      }
      Serial.println("\nConnecté sur WiFi.");
      Serial.print("IP Address: ");
      Serial.println(WiFi.localIP());
    }
    
    bool APIManager::getData(const String& api_path) {
      if (WiFi.status() == WL_CONNECTED) {
        WiFiClient client;
        HTTPClient http;

        // Initialise la connexion HTTP
        http.begin(client, serverUrl + api_path);

        // Envoyer la requête HTTP GET
        int httpResponseCode = http.GET();

        if (httpResponseCode == 200) {
          // Le serveur est en bonne santé
          http.end();
          return true;
        } else {
          // Le serveur n'est pas en bonne santé
          http.end();
          return false;
        }
      } else {
        Serial.println("WiFi déconnecté!");
        return false;
      }
    }
    void APIManager::sendData(const StaticJsonDocument<JSON_SIZE>& jsonDoc, const String& api_path, const String& method) {
      // Vérifie si le WiFi est connecté
      if (WiFi.status() == WL_CONNECTED) {
        WiFiClient client;
        HTTPClient http;

        // Initialise la connexion HTTP
        http.begin(client, serverUrl + api_path);
        http.addHeader("Content-Type", "application/json");

        String jsonString;
        serializeJson(jsonDoc, jsonString);

        // Envoyer la requête HTTP POST
        int httpResponseCode = -1;
        if(method == "POST")
          httpResponseCode = http.POST(jsonString);

        if (httpResponseCode > 0) {
          // Affiche le code de réponse HTTP et la réponse
          Serial.print("Code de réponse HTTP : ");
          Serial.println(httpResponseCode);
          String payload = http.getString();
          Serial.println("Réponse: " + payload);
        } else {
          Serial.print("Code d'erreur : ");
          Serial.println(httpResponseCode);
        }

        // Libère les ressources
        http.end();
      } else {
        Serial.println("WiFi déconnecté!");
      }
    }
    bool APIManager::checkActif(const int id) {
      if (WiFi.status() == WL_CONNECTED) {
        WiFiClient client;
        HTTPClient http;

        // Initialise la connexion HTTP
        http.begin(client, serverUrl + "/capteur/" + String(id));

        // Envoyer la requête HTTP GET
        int httpResponseCode = http.GET();

        if (httpResponseCode == 200) {
          // Le serveur est en bonne santé
          String payload = http.getString();
          http.end();

          StaticJsonDocument<512> doc;
          DeserializationError error = deserializeJson(doc, payload);

          if (error) {
              Serial.print("Erro ao analisar JSON: ");
              Serial.println(error.c_str());
              return false;
          }

          if (doc["actif"].as<bool>()) {
              return true;
          } else {
              Serial.println("Capteur inactif!");
              return false;
          }

          return true;
        } else {
          // Le serveur n'est pas en bonne santé
          http.end();
          return false;
        }
      } else {
        Serial.println("WiFi déconnecté!");
        return false;
      }
    }