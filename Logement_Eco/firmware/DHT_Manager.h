#ifndef DHT_MANAGER_H
#define DHT_MANAGER_H

#include <Arduino.h>
#include <DHT.h>

/**
 * @brief Classe pour gérer le capteur DHT de manière non bloquante
 */
class DHTManager {
  private:
    uint8_t pin; ///< Broche du capteur DHT
    uint8_t type; ///< Type de capteur DHT (DHT11, DHT22)
    DHT dht; ///< Instance du capteur DHT
    float temp; ///< Dernière valeur de température
    float hum; ///< Dernière valeur d'humidité
    unsigned long last_time; ///< Dernière fois que les données ont été mises à jour
    unsigned long interval; ///< Intervalle entre les lectures (en millisecondes)

  public:
    /**
     * @brief Constructeur pour initialiser la classe avec des paramètres personnalisés
     * 
     * @param pin Broche pour la connexion du capteur DHT
     * @param type Type du capteur (ex. DHT11, DHT22)
     * @param interval Intervalle entre les lectures (en ms)
     */
    DHTManager(uint8_t pin, uint8_t type, unsigned long interval);

    /**
     * @brief Initialise le capteur DHT
     */
    void begin();

    /**
     * @brief Met à jour les données du capteur à intervalles réguliers
     * 
     * @return true si les données ont changé, false sinon
     */
    bool update();

    /**
     * @brief Obtient la température actuelle
     * 
     * @return La température en degrés Celsius
     */
    float getTemperature();

    /**
     * @brief Obtient l'humidité actuelle
     * 
     * @return Le pourcentage d'humidité
     */
    float getHumidity();
};

#endif
