#ifndef WIFISNIFFER_H
#define WIFISNIFFER_H

#include <ESP8266WiFi.h>
#include <ArduinoJson.h>

/**
 * @brief Structure contenant les informations d'un réseau WiFi.
 */
struct NetworkInfo {
  String ssid;   ///< Nom du réseau WiFi
  String bssid;  ///< Adresse MAC du point d'accès
  int rssi;      ///< Puissance du signal
  float distance;///< Distance estimée basée sur le RSSI
};

/**
 * @brief Classe pour gérer le sniffing WiFi et l'estimation de la distance.
 */
class WiFiSniffer {
  private:
    NetworkInfo* networks; ///< Tableau des réseaux détectés
    int numNetworks;       ///< Nombre de réseaux détectés
    int limitsNetworks[2]; ///< Limites pour le nombre de réseaux à détecter
    void sortNetworks();   ///< Méthode pour trier les réseaux par RSSI

  public:
    /**
     * @brief Constructeur de la classe WiFiSniffer.
     * @param min Nombre minimum de réseaux à détecter
     * @param max Nombre maximum de réseaux à détecter
     */
    WiFiSniffer(int min = 3, int max = 6);

    /**
     * @brief Destructeur de la classe WiFiSniffer.
     */
    ~WiFiSniffer();

    /**
     * @brief Méthode pour scanner les réseaux WiFi disponibles.
     */
    void scanNetworks();

    /**
     * @brief Méthode pour scanner et trier les réseaux WiFi disponibles.
     * @return true si le scan et le tri sont réussis, false sinon
     */
    bool scanAndSortNetworks();

    /**
     * @brief Méthode pour estimer la distance basée sur le RSSI.
     * @param rssi Puissance du signal
     * @param rssi_ref Référence RSSI (par défaut -40)
     * @param n Facteur d'atténuation (par défaut 2.0)
     * @return Distance estimée
     */
    float calculateDistance(int rssi, int rssi_ref = -40, float n = 2.0);

    /**
     * @brief Méthode pour détecter les points d'accès publics.
     * @param publicSSID SSID du point d'accès public
     */
    void detectPublicAPs(const String& publicSSID);

    /**
     * @brief Génère une chaîne JSON contenant les informations des réseaux détectés.
     * @return Chaîne JSON
     */
    String generateJSON();

    /**
     * @brief Définit les limites pour le nombre de réseaux à détecter.
     * @param min Nombre minimum de réseaux
     * @param max Nombre maximum de réseaux
     */
    void setLimits(int min, int max);

    /**
     * @brief Obtient les limites pour le nombre de réseaux à détecter.
     * @return Tableau des limites
     */
    const int* getLimits() { return limitsNetworks; }

    /**
     * @brief Obtient le nombre de réseaux détectés.
     * @return Nombre de réseaux détectés
     */
    int getNumNetworks() { return numNetworks; }
};

#endif