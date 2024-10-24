#include "DHT_Manager.h"
#include "LoRaModule.h"    // Inclure la bibliothèque pour la gestion du module LoRa

// Définition des broches pour la communication série avec le modem LoRa
#define LORA_RX D5  // RX du modem LoRa connecté au TX de l'ESP8266
#define LORA_TX D6  // TX du modem LoRa connecté au RX de l'ESP8266
#define DEV_EUI "70B3D57ED006AF94"
#define APP_EUI "155E688412EB473C"
#define APP_KEY "3553D5B3A2F8B4A2DD6ED4DA9B68BCA1"
#define MAX_TRIES 5
#define DATA_RATE 1 // DOIT ETRE 1 ,2 ,3 ,4 ou 5
// Création de l'instance du module LoRa avec les informations de configuration
LoRaModule lora(DEV_EUI, APP_EUI, APP_KEY, LORA_RX, LORA_TX, MAX_TRIES, ("DR"+String(DATA_RATE)));


#define DHTPIN D4     // Broche de données du capteur DHT11
#define DHTTYPE DHT11 // Type de capteur DHT
// Création de l'instance du capteur DHT avec 5000ms d'interval
DHTManager dht(DHTPIN, DHTTYPE, 5000);

void setup() {
  delay(100);
  Serial.begin(115200);  // Initialisation de la communication série pour le débogage
  lora.setupLoRaModule(); // Configuration du modem LoRa
  bool resp = false;
  while(!resp)
    resp = lora.joinNetwork(); // Tentative de connexion au réseau LoRa
  // Initialize DHT sensor
  dht.begin();
}

void loop() {
  if (dht.update()) {
    // Si les données ont changé, les envoyer par MQTT
    Serial.print("Temperature: ");
    Serial.println(dht.getTemperature());
    Serial.print("Humidity: ");
    Serial.println(dht.getHumidity());
    // Exemple de publication MQTT
    String data = "<"+String(dht.getTemperature()) + ";" + String(dht.getHumidity())+">";
    lora.sendToLoRa(data,3000);
    String response = lora.checkResponse();
  }
  delay(5000);
}