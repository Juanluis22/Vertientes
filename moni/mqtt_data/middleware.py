# Importar las bibliotecas necesarias
from django.http import StreamingHttpResponse  # Para enviar respuestas en tiempo real
import paho.mqtt.client as mqtt  # Biblioteca para trabajar con MQTT
import json  # Para manejar datos en formato JSON
from queue import Queue  # Para manejar una cola de mensajes

from .models import datos  # Importa el modelo 'datos'

# Crear una cola global para almacenar los mensajes recibidos de MQTT
message_queue = Queue()

# Definir el middleware MQTT
class MQTTMiddleware:
    # Constructor del middleware
    def __init__(self, get_response):
        # Guardar la función get_response para procesar la solicitud
        self.get_response = get_response

        # Configuración del broker MQTT
        self.mqtt_server = "broker.emqx.io"
        self.mqtt_port = 1883
        self.mqtt_user = ""  # Usuario del broker (si es necesario)
        self.mqtt_password = ""  # Contraseña del broker (si es necesario)
        self.mqtt_topic = "Salida/01"  # Tópico al que se suscribirá

        # Crear una instancia del cliente MQTT
        self.client = mqtt.Client()
        # Definir las funciones callback para cuando se conecte y reciba mensajes
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        print("Instancia de cliente creada")

        # Conectar al broker MQTT
        self.client.connect(self.mqtt_server, self.mqtt_port, 60)
        print("Se conecto con el broker")

        # Iniciar el loop del cliente MQTT en segundo plano
        # Esto permite que el cliente escuche mensajes en todo momento
        self.client.loop_start()

    # Esta función se llama cada vez que se procesa una solicitud
    def __call__(self, request):
        return self.get_response(request)

    # Función callback que se llama cuando el cliente se conecta al broker
    def on_connect(self, client, userdata, flags, rc):
        print(f"Conectado con el código: {rc}")
        # Una vez conectado, suscribirse al tópico deseado
        client.subscribe(self.mqtt_topic)

    # Función callback que se llama cuando el cliente recibe un mensaje del broker
    def on_message(self, client, userdata, msg):
        # Decodificar el mensaje
        payload_str = msg.payload.decode()
        
       
        try:
            # Intenta convertir la cadena a un diccionario
            message_dict = json.loads(payload_str)
            data = json.loads(msg.payload)
            # Guardar los datos en la base de datos
            datos.objects.create(
                caudal=data["caudal"],
                pH=data["pH"],
                conductividad=data["conductividad"],
                turbiedad=data["turbiedad"],
                temperatura=data["temperatura"],
                humedad=data["humedad"],
                vertiente_id=1,#data["vertiente_id"], Cambiar por el ID de la vertiente
            )
            datos.save()
            
        except json.JSONDecodeError:
            # Si hay un error, simplemente usa la cadena tal como está
            message_dict = {"message": payload_str}
        # Agregar el diccionario a la cola
        message_queue.put(message_dict)
        print("Mensaje recibido")

