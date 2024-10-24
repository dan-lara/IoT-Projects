#ifndef WIFISNIFFER_H
#define WIFISNIFFER_H

#include <ESP8266WiFi.h>
#include <ArduinoJson.h>
// Classe pour gérer le sniffing WiFi et l'estimation de la distance
class WiFiSniffer {
  public:
    WiFiSniffer();  // Constructeur

    // Méthode pour scanner les réseaux WiFi disponibles
    void scanNetworks();

    // Méthode pour estimer la distance basée sur le RSSI
    float calculateDistance(int rssi, int rssi_ref = -40, float n = 2.0);

    // Méthode pour détecter les points d'accès publics
    void detectPublicAPs(const String& publicSSID);
    String generateJSON(const String&);
};

#endif
