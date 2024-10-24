#ifndef LORAMODULE_H
#define LORAMODULE_H

#include <Arduino.h>
#include <SoftwareSerial.h>

/**
 * @class LoRaModule
 * @brief Classe pour gérer la communication avec un module LoRa E5.
 */
class LoRaModule {
  private:
    String dev_eui;
    String app_eui;
    String app_key;
    String frequency;   // Fréquence définie (par défaut EU868)
    String data_rate;   // Data Rate (DR1 à DR5)
    SoftwareSerial lora_serial;
    int max_attempts;

  public:
    /**
     * @brief Constructeur de la classe LoRaModule.
     * @param dev_eui Identifiant unique du périphérique LoRa.
     * @param app_eui Identifiant de l'application LoRa.
     * @param app_key Clé de l'application pour l'authentification.
     * @param rx_pin Pin RX pour SoftwareSerial.
     * @param tx_pin Pin TX pour SoftwareSerial.
     * @param max_attempts Nombre maximum de tentatives de connexion.
     * @param data_rate Data rate utilisé pour la transmission (par défaut "DR3").
     * @param frequency Fréquence utilisée pour la communication LoRa (par défaut "EU868").
     */
    LoRaModule(String dev_eui, String app_eui, String app_key, int rx_pin, int tx_pin, int max_attempts = 3, String data_rate = "DR3", String frequency = "EU868");

    /**
     * @brief Initialiser le module LoRa avec les paramètres définis.
     */
    void setupLoRaModule();

    /**
     * @brief Tenter de se connecter au réseau LoRa.
     * @return true si la connexion réussit, false sinon.
     */
    bool joinNetwork();

    /**
     * @brief Reconnecter le module en cas d'échec.
     */
    void reconnect();

    /**
     * @brief Envoyer des données au module LoRa.
     * @param data Données à envoyer sous forme de chaîne JSON.
     * @param delay_ms Délai avant la prochaine commande en millisecondes.
     * @param mode Mode d'envoi des données (par défaut "MSG").
     */
    void sendToLoRa(String data, int delay_ms, String mode="MSG");

    /**
     * @brief Vérifier la réponse du module LoRa.
     * @param expected Réponse attendue pour valider le succès.
     * @return true si la réponse correspond à celle attendue, false sinon.
     */
    String checkResponse(String expected="");
};

#endif // LORAMODULE_H
