#include "DHT_Manager.h"

/**
 * @brief Constructeur de la classe DHTManager
 * 
 * @param pin Broche à laquelle le capteur DHT est connecté
 * @param type Type du capteur DHT (ex. DHT11, DHT22)
 * @param interval Temps en millisecondes entre chaque lecture de capteur
 */
DHTManager::DHTManager(uint8_t pin, uint8_t type, unsigned long interval)
  : pin(pin), type(type), dht(pin, type), interval(interval), last_time(0), temp(NAN), hum(NAN) {}

/**
 * @brief Initialise le capteur DHT
 */
void DHTManager::begin() {
  dht.begin();
}

/**
 * @brief Lit et met à jour les données du capteur si l'intervalle de temps est dépassé
 * 
 * @return true si les nouvelles données sont différentes des précédentes, false sinon
 */
bool DHTManager::update() {
  unsigned long current_time = millis();
  if (current_time - last_time >= interval) {
    last_time = current_time;

    float newT = dht.readTemperature();
    float newH = dht.readHumidity();

    if (!isnan(newT)) temp = newT;
    if (!isnan(newH)) hum = newH;

    return true;
  }
  return false;
}

/**
 * @brief Retourne la dernière température lue
 * 
 * @return Température en degrés Celsius
 */
float DHTManager::getTemperature() {
  return temp;
}

/**
 * @brief Retourne la dernière humidité lue
 * 
 * @return Humidité en pourcentage
 */
float DHTManager::getHumidity() {
  return hum;
}
