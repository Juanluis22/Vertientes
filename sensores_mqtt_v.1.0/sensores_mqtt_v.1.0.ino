#include <ArduinoJson.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include "DHT.h"

//Clientes de Wifi y MQTT
WiFiClient espClient;
PubSubClient mqttClient(espClient);

// Configuración WiFi
const char* ssid = "JESUS Y VALE-2.4G";
const char* password = "eduardo1";

// Configuración MQTT
const char* mqtt_server = "broker.emqx.io";
const int mqtt_port = 1883;
const char* mqtt_user = "";
const char* mqtt_password = "";
const char* mqtt_topic_sub = "Entrada/01";
const char* mqtt_topic_pub = "Salida/01";

// Configuración de Pines
#define DHTPIN 15
#define DHTTYPE DHT11
#define PH_PIN 2
#define FLOW_PIN 4
#define TURBIDITY_PIN 13

//Variables
DHT dht(DHTPIN, DHTTYPE);
volatile int pulseCount = 0; //Variables de flujo
float flowRate;//Variables de flujo
unsigned long lastFlowRateCheck = 0;//Variables de flujo
float factor_conversion = 7.5; // Factor de conversión para el sensor de flujo

//DATA.JSON
StaticJsonDocument<130> data; // Crear un documento JSON DINAMICO para almacenar los datos
//DynamicJsonDocument data(256);  // Crear un documento JSON DINAMICO para almacenar los datos
char output[130];


void setup() {
  Serial.begin(115200);
  wifiInit();
  
  //Conexiones wi-fi y MQTT
  mqttClient.setServer(mqtt_server,mqtt_port);
  mqttClient.setCallback(callback);

  //Sensores
  dht.begin();
  pinMode(FLOW_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(FLOW_PIN), pulseCounter, RISING);

  Serial.println(F("{DHT11,pH,caudal,turbidez} test KIT 01 CON MQTT"));

}

void loop() {
  if (!mqttClient.connected()) {
    Serial.print("Disconected from MQTT...");
    reconnect();
  }

  // Limpia el documento JSON antes de llenarlo con nuevos datos
  data.clear();

  mqttClient.loop();
  delay(2500);

  //LECTURA DE SENSORES
  colectData();
  // Enviar datos recopilados
  sendData();
  
}

//FUNCIONES DE CONEXION WI-FI Y MQTT
void wifiInit() {
    Serial.print("Conectándose a ");
    Serial.println(ssid);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
      Serial.print(".");
        delay(500);  
    }
    Serial.println("");
    Serial.println("Conectado a WiFi");
    Serial.println("Dirección IP: ");
    Serial.println(WiFi.localIP());
    int rssi = WiFi.RSSI();
    Serial.print("Señal WiFi (RSSI): ");
    Serial.print(rssi);
    Serial.println(" dBm");
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Mensaje recibido [");
  Serial.print(topic);
  Serial.print("] ");

  char payload_string[length + 1];
  memcpy(payload_string, payload, length);
  payload_string[length] = '\0';

  // Parsear el payload a un objeto JSON
  DynamicJsonDocument receivedData(256);
  DeserializationError error = deserializeJson(receivedData, payload_string);

  // Verificar si hubo un error al parsear el JSON
  if (error) {
    Serial.print(F("deserializeJson() failed: "));
    Serial.println(error.c_str());
    return;
  }
  else{
    // Ahora puedes acceder a los valores del JSON usando receivedData
    serializeJson(receivedData, Serial);
  }
}

void reconnect() {
  while (!mqttClient.connected()) {
    Serial.print("Triying to conect MQTT...");
    String clientId = "ESP32Client-";
    clientId += String((uint32_t)ESP.getEfuseMac(), HEX); 

    if (mqttClient.connect(clientId.c_str())) {
      Serial.println("Connected");

      mqttClient.subscribe(mqtt_topic_sub);
      Serial.println("-----------------------------");
      Serial.println("Conected to: "+ String(mqtt_topic_sub));
      Serial.println("-----------------------------");
      
    } else {
      Serial.print("Fallo, rc=");
      Serial.print(mqttClient.state());
      Serial.println("try again in 4 seconds...");
      // Wait 4 seconds before retrying
      delay(4000);
    }
  }
}

//RECOLECTA TODOS LOS DATOS DE SENSORES
void colectData() {
  // Medición de Humedad y Temperatura
  medirDth11();
  // Medición de pH
  medirPh();
  // Medición de Caudal
  medirCaudal();
  // Medición de Turbidez
  medirTurbidez();
  // Imprimir el documento JSON
  //serializeJson(data, Serial);
  Serial.println();  // Nueva línea para una mejor visualización
}


//PUBLICA EL DOCUMENTO JSON EN MQTT
void sendData() {
  char buffer[256];
  serializeJson(data, buffer);
  mqttClient.publish(mqtt_topic, buffer);
}


//FUNCIONES DE SENSORES
void medirDth11() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  if (isnan(h) || isnan(t)) {
    Serial.println(F("Failed to read from DHT11!"));
    return;
  }

  data["humidity"] = h;
  data["temperature"] = t;
}

void medirPh() {
  float ph = sensor_ph();
  if (isnan(ph)) {
    Serial.println(F("Failed to read pH!"));
    return;
  }

  data["pH"] = ph;
}


float sensor_ph() {
  int valor = analogRead(PH_PIN);
  float ph = map(valor, 0, 4095, 0, 140) / 10.0;
  return ph;
}

void pulseCounter() {
  pulseCount++;
}

float medirTurbidez() {
  int turbidityValue = analogRead(TURBIDITY_PIN);

  if (isnan(turbidityValue)) {
    Serial.println(F("Failed to read from Turbidity sensor!"));
    return 0.0;
  }

  data["turbidity"] = turbidityValue;
  return turbidityValue;
}

void medirCaudal() {
  // Desactivar interrupciones para medir el caudal
  detachInterrupt(digitalPinToInterrupt(FLOW_PIN));

  // Calcular el caudal en L/min
  flowRate = ((1000.0 / (millis() - lastFlowRateCheck)) * pulseCount) / 450.0;

  // Actualizar el tiempo de la última medición y resetear el contador de pulsos
  lastFlowRateCheck = millis();
  pulseCount = 0;

  // Reactivar las interrupciones
  attachInterrupt(digitalPinToInterrupt(FLOW_PIN), pulseCounter, RISING);

  // Calcular el caudal en L/h
  //float caudal_L_h = flowRate * 60;

  // Verificar si el caudal es un número válido
  if (isnan(flowRate)) {
    Serial.println(F("Failed to read from Caudal!"));
    return;
  }

  data["flowRate_L/min"] = flowRate;
  //data["flowRate_L/h"] = caudal_L_h;
}



























