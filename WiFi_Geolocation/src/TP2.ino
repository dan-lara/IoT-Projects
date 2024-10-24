#include "WiFiSniffer.h"   // Inclure la bibliothèque pour le sniffing WiFi
#include "LoRaModule.h"    // Inclure la bibliothèque pour la gestion du module LoRa
#include <ArduinoJson.h>

// Définition des broches pour la communication série avec le modem LoRa
#define LORA_RX D5  // RX du modem LoRa connecté au TX de l'ESP8266
#define LORA_TX D6  // TX du modem LoRa connecté au RX de l'ESP8266
#define DEV_EUI "70B3D57ED006AEE5"
#define APP_EUI "C4B2074C385B7F6A"
#define APP_KEY "2BD9D746199C68C2011BA6250B4B5EF2"
#define MAX_TRIES 5
#define DATA_RATE 4 // DOIT ETRE 2,3,4 ou 5
// Initialisation de l'instance du sniffer WiFi
WiFiSniffer sniffer(3,6);

// Création de l'instance du module LoRa avec les informations de configuration
LoRaModule lora(DEV_EUI, APP_EUI, APP_KEY, LORA_RX, LORA_TX, MAX_TRIES, ("DR"+String(DATA_RATE)));

void setup() {
  delay(100);
  Serial.begin(115200);  // Initialisation de la communication série pour le débogage
  lora.setupLoRaModule(); // Configuration du modem LoRa
  bool resp = false;
  while(!resp)
    resp = lora.joinNetwork(); // Tentative de connexion au réseau LoRa

  int maxNets;
  if (DATA_RATE < 3){
    Serial.println("Data rate doit etre 3 ou plus");
    while(1); // Boucle infinie si le taux de données est inférieur à 3
  }
  else {
    switch(DATA_RATE){
      case 2:
        maxNets = 2;
        break;
      case 3:
        maxNets = 6;
        break;
      case 4:
        maxNets = 13;
        break;
      case 5:
        maxNets = 14;
        break;
    }
    Serial.println("Max. reseaux:" + String(maxNets));
    sniffer.setLimits(3, maxNets); // Définir les limites du sniffer WiFi
  }
  Serial.println("Configuration terminée, démarrage du scan WiFi...");
}

/**
 * Boucle principale du programme.
 * 
 * Cette fonction effectue les opérations suivantes :
 * 1. Scanne les réseaux WiFi disponibles et génère un JSON avec les données détectées.
 * 2. Formate les données JSON pour l'envoi via LoRa.
 * 3. Envoie les données formatées au modem LoRa avec un délai de 5 secondes.
 * 4. Vérifie et affiche la réponse du modem LoRa.
 * 5. Attend 5 secondes avant de recommencer le processus.
 */
void loop() {
  // Générer un JSON avec les données des réseaux détectés
  sniffer.scanNetworks();
  String jsonData = sniffer.generateJSON();

  // Formater les données JSON pour l'envoi via LoRa 
  // Par exemple, "<2/ABCDE12345,-40;ABCDE67893,-79>"
  String data = formatToLoRa(jsonData);

  // Envoyer les données au gateway LoRa avec un délai de 5s
  Serial.println("Envoi des données : " + data);
  lora.sendToLoRa(data, 5000);

  // Vérifier et afficher la réponse du gateway LoRa
  String response = lora.checkResponse();
  delay(5000);
}


/**
 * Formater les données JSON pour l'envoi via LoRa.
 * 
 * @param jsonData Les données JSON à formater.
 * @return Une chaîne de caractères formatée pour l'envoi via LoRa.
 */
String formatToLoRa(const String& jsonData) {
  // Créer un document JSON basé sur la taille du JSON d'entrée
  DynamicJsonDocument doc(1024);
  deserializeJson(doc, jsonData);

  // Créer une chaîne vide pour stocker les données formatées
  String formattedString = "<";
  
  // Boucler à travers chaque réseau dans le tableau "Networks"
  JsonArray networks = doc["Networks"].as<JsonArray>();

  int numNetworks = networks.size();
  formattedString += String(numNetworks) + "/";

  for (size_t i = 0; i < numNetworks; ++i) {

    String mac = networks[i]["MAC"].as<String>();
    mac.replace(":", "");

    String rssi = networks[i]["RSSI"].as<String>();

    // Ajouter MAC et RSSI à la chaîne formatée
    formattedString += mac + "," + rssi;

    // Si ce n'est pas le dernier réseau, ajouter un séparateur point-virgule
    if (i < numNetworks - 1)
      formattedString += ";";
  }

  // Fermer le format avec ">"
  formattedString += ">";

  return formattedString;
}