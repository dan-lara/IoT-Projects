#include "API_Manager.h"
#include "DHT_Manager.h"

#define DHTPIN D5     // Broche de données du capteur DHT11
#define DHTTYPE DHT11 // Type de capteur DHT

// Configuration
const char* WIFI_SSID = "SSID";
const char* WIFI_PASSWORD = "PASSWORD";
const String API_URL = "http://192.168.0.1:8000";
const int CAPTEUR_ID = 6;

APIManager api(WIFI_SSID, WIFI_PASSWORD, API_URL);
DHTManager dht(DHTPIN, DHTTYPE, 20000); // DHT11 connecté à D4, intervalle 2s

void setup() {
  Serial.begin(115200);

  api.begin();
  dht.begin();
}
StaticJsonDocument<JSON_SIZE> prepareJSON_mesure(int id_c, float valeur);
void loop() {
    if (dht.update()) {
      if (api.getData()){
        float temperature = dht.getTemperature();
        Serial.print("Température: ");
        Serial.println(temperature);

        if(api.checkActif(CAPTEUR_ID))
          api.sendData(prepareJSON_mesure(CAPTEUR_ID, temperature), "/mesure/");
        
        float humidity = dht.getHumidity();
        Serial.print("Humidité: ");
        Serial.println(humidity);

        if(api.checkActif(CAPTEUR_ID+1))
          api.sendData(prepareJSON_mesure(CAPTEUR_ID+1, humidity), "/mesure/");
      }
      else{
        Serial.println("Error to find Server");
      }

    }
}

StaticJsonDocument<JSON_SIZE> prepareJSON_mesure(int id_c, float valeur){
  StaticJsonDocument<JSON_SIZE> jsonDoc;
  jsonDoc["id_c"] = id_c;
  jsonDoc["valeur"] = valeur;
  return jsonDoc;
}