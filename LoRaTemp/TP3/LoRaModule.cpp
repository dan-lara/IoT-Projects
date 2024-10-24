#include "LoRaModule.h"

/**
 * @brief Constructeur de la classe LoRaModule.
 */
LoRaModule::LoRaModule(String dev_eui, String app_eui, String app_key, int rx_pin, int tx_pin, int max_attempts, String data_rate, String frequency) 
  : dev_eui(dev_eui), app_eui(app_eui), app_key(app_key), frequency(frequency), data_rate(data_rate), 
    lora_serial(rx_pin, tx_pin), max_attempts(max_attempts) {}

/**
 * @brief Initialiser le module LoRa avec les paramètres définis.
 */
void LoRaModule::setupLoRaModule() {
  lora_serial.begin(9600);  // Démarrer la communication série avec le module LoRa
  delay(1000);

  sendToLoRa("AT+ID", 1000,"config");
  sendToLoRa("AT+ID=DevEui,\"" + dev_eui + "\"", 1000,"config");
  sendToLoRa("AT+ID=AppEui,\"" + app_eui + "\"", 1000,"config");
  sendToLoRa("AT+KEY=APPKEY,\"" + app_key + "\"", 1000,"config");
  sendToLoRa("AT+MODE=LWOTAA", 1000,"config");
  sendToLoRa("AT+DR=" + data_rate, 1000,"config");  // Paramétrer le Data Rate (DR1 à DR5)
}

/**
 * @brief Tenter de se connecter au réseau LoRa.
 * @return true si la connexion réussit, false sinon.
 */
bool LoRaModule::joinNetwork() {
  for (int attempt = 0; attempt < max_attempts; attempt++) {
    // Serial.println("Tentative de connexion au réseau LoRa (" + String(attempt + 1) + "/" + String(max_attempts) + ")");
    sendToLoRa("AT+JOIN", 3000, "config");

    String expected_response  = "+JOIN: Network joined";
    String expected_response2 = "+JOIN: Joined already";
    String response = checkResponse("");

    if (response.indexOf(expected_response) != -1 ||response.indexOf(expected_response2) != -1 ) {
      Serial.println("Connexion réussie au réseau LoRa.");
      return true;
    } else {
      Serial.println("Échec de la connexion. Nouvelle tentative...");
    }
  }
  
  // Si toutes les tentatives échouent
  Serial.println("Connexion au réseau LoRa échouée après " + String(max_attempts) + " tentatives.");
  return false;
}

/**
 * @brief Reconnecter le module en cas d'échec.
 */
void LoRaModule::reconnect() {
  Serial.println("Réinitialisation du module et nouvelle tentative de configuration...");
  setupLoRaModule();  // Réinitialiser la configuration du module
  joinNetwork();
}

/**
 * @brief Envoyer des données au module LoRa.
 * @param data Données à envoyer sous forme de String.
 * @param delay_ms Délai avant la prochaine commande en millisecondes.
 * @param mode Mode d'envoi des données ("MSG" pour message, autre pour commande).
 */
void LoRaModule::sendToLoRa(String data, int delay_ms, String mode) {
  if (mode == "MSG")
    lora_serial.println("AT+MSG=\"" + data + "\"");
  else
    lora_serial.println(data);
  delay(delay_ms);  // Attendre le délai spécifié avant la prochaine commande
}

/**
 * @brief Vérifier la réponse du module LoRa.
 * @param expected Réponse attendue pour valider le succès (si vide, retourne simplement la réponse).
 * @return true si la réponse correspond à celle attendue, false sinon.
 */
String LoRaModule::checkResponse(String expected) {
  String response = "";
  Serial.println("Reponse du module: ");
  while (lora_serial.available()) {
    response += lora_serial.readString() +"\n";
    Serial.println("Réponse du module LoRa :\n" + response);
  }
  // Serial.println("Réponse du module LoRa : " + response);

  if (expected == "") {
    return response;  // Si aucune réponse attendue n'est spécifiée, renvoyer simplement la réponse.
  }

  return (response.indexOf(expected) != -1) ? "OK" : "FAIL";
}
