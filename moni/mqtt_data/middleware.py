
# Importar las bibliotecas necesarias
from django.http import StreamingHttpResponse  # Para enviar respuestas en tiempo real
import paho.mqtt.client as mqtt  # Biblioteca para trabajar con MQTT
import json  # Para manejar datos en formato JSON
from queue import Queue  # Para manejar una cola de mensajes

# Importa el modelo 'datos', 'kit' y 'vertiente' de la aplicación 'nucleo'
from nucleo.models import vertiente, kit, datos



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

    def save_data(self,data):
        # Comparar data[mac] con el atributo mac de la entidad kit para asignar el id de la vertiente correspondiente
        # Recuperar el ID (Direccion MAC) del mensaje recibido
        data_mac = data.get("mac", None)
        if not data_mac:
            print("Error: No se encontró la clave 'mac' en los datos recibidos.")
            return

        # Buscar el kit que tenga esa mac
        try:
            data_kit = kit.objects.get(mac=data_mac)
        except kit.DoesNotExist:
            print("Error: No se encontró el kit con la mac recibida.")
            return
        except kit.MultipleObjectsReturned:
            print("Error: Se encontraron múltiples kits con la misma MAC.")
            return
        kit_id = data_kit.id

        # Obtiene el ID de la vertiente asociada a ese kit
        vertiente_id = data_kit.vertiente_id
        vertiente_instance = vertiente.objects.get(id=vertiente_id)



        # mostrar cual es el dato que falta
        if not ("flow_Rate" in data):
            print("Falta el caudal")
        if not ("pH" in data): 
            print("Falta el pH")
        if not ("turbidity" in data):
            print("Falta la turbidez")
        if not ("temperature" in data):
            print("Falta la temperatura")
        if not ("humidity" in data):
            print("Falta la humedad")
        if not ("mac" in data):
            print("Falta la MAC")

        print("Datos válidos")

        # Guardar los datos
        dato = datos(
            caudal=data["caudal"],
            pH=data["pH"],
            conductividad=data["conductividad"],
            turbiedad=data["turbiedad"],
            temperatura=data["temperatura"],
            humedad=data["humedad"],

            mac=data["mac"],
            kit=data_kit,
            vertiente=vertiente_instance
        )
        dato.save()
        print("Datos guardados exitosamente")


    # Función callback que se llama cuando el cliente recibe un mensaje del broker
    def on_message(self, client, userdata, msg):
        print("Mensaje recibido")
        # Decodificar el mensaje
        payload_str = msg.payload.decode()
        #Guardar los datos que llegan en el modelo datos
       
        try:
            # Intenta convertir la cadena a un diccionario
            message_dict = json.loads(payload_str)
            #Guardar los datos que llegan en el modelo datos
            # Llamar a la función save_data
            self.save_data(message_dict)
    
        except json.JSONDecodeError:
            # Si hay un error, simplemente usa la cadena tal como está
            message_dict = {"message": payload_str}
            print("Error al decodificar el mensaje")
        # Agregar el diccionario a la cola
        message_queue.put(message_dict)
