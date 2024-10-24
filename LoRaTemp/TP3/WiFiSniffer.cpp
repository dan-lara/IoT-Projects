#include "WiFiSniffer.h"

// Constructeur
WiFiSniffer::WiFiSniffer() {
  WiFi.mode(WIFI_STA);  // Définir le mode Station
  WiFi.disconnect();    // Assurez-vous qu'il n'est connecté à aucun réseau
  delay(100);
}

// Méthode pour scanner les réseaux WiFi disponibles
void WiFiSniffer::scanNetworks() {
  Serial.println("Début de la recherche de réseaux WiFi...");
  int n = WiFi.scanNetworks();
  
  Serial.println("Recherche terminée !");
  if (n == 0) {
    Serial.println("Aucun réseau trouvé");
  } else {
    Serial.println("Réseaux trouvés :");
    for (int i = 0; i < n; ++i) {
      Serial.print(i + 1);
      Serial.print(": ");
      Serial.print(WiFi.SSID(i));  // Nom du réseau
      Serial.print("[(");
      Serial.print(calculateDistance(WiFi.RSSI(i)));
      Serial.print(" m), (");
      Serial.print(WiFi.RSSI(i));  // Intensité du signal
      Serial.print(" dBm)] MAC: ");
      Serial.println(WiFi.BSSIDstr(i));  // Adresse MAC
    }
  }
}

// Méthode pour estimer la distance basée sur le RSSI
float WiFiSniffer::calculateDistance(int rssi, int rssi_ref, float n) {
  return pow(10, (rssi_ref - rssi) / (10.0 * n));
}

// Méthode pour détecter les points d'accès publics
void WiFiSniffer::detectPublicAPs(const String& publicSSID) {
  Serial.println("Détection des points d'accès publics...");
  int n = WiFi.scanNetworks();
  
  for (int i = 0; i < n; ++i) {
    // Si le SSID correspond au réseau public
    if (WiFi.SSID(i) == publicSSID) {
      Serial.print("Point d'accès public trouvé : ");
      Serial.println(WiFi.SSID(i));
      Serial.print("MAC : ");
      Serial.println(WiFi.BSSIDstr(i));  // Afficher l'adresse MAC
      Serial.print("Distance: ");
      Serial.print(calculateDistance(WiFi.RSSI(i)));
      Serial.println(" m");
    }
  }
}

String WiFiSniffer::generateJSON(const String& ID) {
  JsonDocument doc;
  doc["ID"] = ID;
  int n = WiFi.scanNetworks();
  doc["Quantite"] = n;
  for (int i = 0; i < n; ++i) {
    doc["Networks"][i]["MAC"] = WiFi.BSSIDstr(i);
    doc["Networks"][i]["SSID"] = WiFi.SSID(i);
    doc["Networks"][i]["RSSI"] = WiFi.RSSI(i);

  }
  String jsonString;
  serializeJson(doc, jsonString);
  return jsonString;
}
