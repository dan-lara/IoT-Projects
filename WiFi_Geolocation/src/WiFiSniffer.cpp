#include "WiFiSniffer.h"

// Constructeur
WiFiSniffer::WiFiSniffer(int min, int max) : networks(nullptr), numNetworks(0) {
  setLimits(min, max);
  WiFi.mode(WIFI_STA);  // Définir le mode Station
  WiFi.disconnect();    // Assurez-vous qu'il n'est connecté à aucun réseau
  delay(100);
}

// Destructeur
WiFiSniffer::~WiFiSniffer() {
  if (networks != nullptr)
    delete[] networks;
}

// Méthode pour définir les limites min et max
void WiFiSniffer::setLimits(int min, int max) {
  limitsNetworks[0] = min;  // Min
  limitsNetworks[1] = max;  // Max
}

// Méthode pour scanner et trier les réseaux WiFi
bool WiFiSniffer::scanAndSortNetworks() {
  if (networks != nullptr) {
    delete[] networks;
    networks = nullptr;
  }
  Serial.println("Début de la recherche de réseaux WiFi...");
  numNetworks = WiFi.scanNetworks();
  Serial.println("Recherche terminée !");   
  if (numNetworks == 0) {
    Serial.println("Aucun réseau trouvé");
    return false;
  }
  // Allouer de la mémoire pour les réseaux
  networks = new NetworkInfo[numNetworks];
  // Stocker les informations des réseaux
  for (int i = 0; i < numNetworks; ++i) {
    networks[i].ssid = WiFi.SSID(i);
    networks[i].bssid = WiFi.BSSIDstr(i);
    networks[i].rssi = WiFi.RSSI(i);
    networks[i].distance = calculateDistance(WiFi.RSSI(i));
  }
  // Trier les réseaux
  sortNetworks();
  // Libérer la mémoire du scan WiFi
  WiFi.scanDelete();
  
  return true;
}

// Méthode pour trier les réseaux par RSSI (signal le plus fort en premier)
void WiFiSniffer::sortNetworks() {
  if (!networks || numNetworks == 0) return;
  
  // Tri à bulles par RSSI
  for (int i = 0; i < numNetworks - 1; i++) 
    for (int j = 0; j < numNetworks - i - 1; j++) 
      if (networks[j].rssi < networks[j + 1].rssi) {
        NetworkInfo temp = networks[j];
        networks[j] = networks[j + 1];
        networks[j + 1] = temp;
      }
}

// Méthode pour scanner les réseaux WiFi disponibles
void WiFiSniffer::scanNetworks() {
  if (!scanAndSortNetworks())
    return;
  Serial.println("Réseaux trouvés :");
  for (int i = 0; i < numNetworks; ++i) {
    Serial.print(i + 1);
    Serial.print(": ");
    Serial.print(networks[i].ssid);
    Serial.print("[(");
    Serial.print(networks[i].distance);
    Serial.print(" m), (");
    Serial.print(networks[i].rssi);
    Serial.print(" dBm)] MAC: ");
    Serial.println(networks[i].bssid);
  }
}

// Méthode pour estimer la distance basée sur le RSSI
float WiFiSniffer::calculateDistance(int rssi, int rssi_ref, float n) {
  return pow(10, (rssi_ref - rssi) / (10.0 * n));
}

// Méthode pour détecter les points d'accès publics
void WiFiSniffer::detectPublicAPs(const String& publicSSID) {
  if (networks == nullptr) {
    if (!scanAndSortNetworks())
      return;
  }
  Serial.println("Détection des points d'accès publics...");
  for (int i = 0; i < numNetworks; i++) {
    if (networks[i].ssid == publicSSID) {
      Serial.print("Point d'accès public trouvé : ");
      Serial.println(networks[i].ssid);
      Serial.print("MAC : ");
      Serial.println(networks[i].bssid);
      Serial.print("Distance: ");
      Serial.print(networks[i].distance);
      Serial.println(" m");
    }
  }
}

// Méthode pour générer un JSON avec les informations des réseaux
String WiFiSniffer::generateJSON() {
  if (networks == nullptr || numNetworks < limitsNetworks[0]) {
    if (!scanAndSortNetworks())
      return "{}";
  }
  JsonDocument doc;
  int n = (numNetworks > limitsNetworks[1]) ? limitsNetworks[1] : numNetworks;

  doc["Quantite"] = n;  
  for (int i = 0; i < n; ++i) {
    doc["Networks"][i]["MAC"] = networks[i].bssid;
    doc["Networks"][i]["SSID"] = networks[i].ssid;
    doc["Networks"][i]["RSSI"] = networks[i].rssi;
  }
  String jsonString;
  serializeJson(doc, jsonString);
  return jsonString;
}