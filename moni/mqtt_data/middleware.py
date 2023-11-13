
# Importar las bibliotecas necesarias
from django.http import StreamingHttpResponse  # Para enviar respuestas en tiempo real
import paho.mqtt.client as mqtt  # Biblioteca para trabajar con MQTT
import json  # Para manejar datos en formato JSON
from queue import Queue  # Para manejar una cola de mensajes

# Importa el modelo 'datos', 'kit' y 'vertiente' de la aplicación 'nucleo'
from nucleo.models import vertiente, kit, datos
#Correo
import moni.settings as setting
from django.template.loader import render_to_string
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from user.models import User
from crud.forms import *


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
        self.mqtt_user = "Vertientes"  # Usuario del broker (si es necesario)
        self.mqtt_password = "vertientes1234"  # Contraseña del broker (si es necesario)
        self.mqtt_topic = "KIT/01"  # Tópico al que se suscribirá

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
        # Diccionario con descripciones para los códigos de retorno
        rc_descriptions = {
            0: "Conexión aceptada.",
            1: "Conexión rechazada, versión de protocolo MQTT incorrecta.",
            2: "Conexión rechazada, identificador de cliente no válido.",
            3: "Conexión rechazada, servidor no disponible.",
            4: "Conexión rechazada, credenciales no válidas.",
            5: "Conexión rechazada, no autorizado."
        }

        # Si rc está en el diccionario, imprime la descripción correspondiente, de lo contrario imprime un mensaje genérico
        print(f"Conexión a MQTT: Código {rc} - {rc_descriptions.get(rc, 'Código desconocido o reservado para usos futuros.')}")

        if rc == 0:  # Solo suscribirse al tópico si la conexión fue exitosa
            client.subscribe(self.mqtt_topic)
        else:
            print("No se suscribirá al tópico debido a un error en la conexión.")


    def send_email(self, user,informacion,problemas,otros):
        data={}
        try:
            # Definir la URL base de tu sitio
            base_url = "http://127.0.0.1:8000/"

            # Definir la ruta específica de la vista que deseas vincular
            ruta = "/inicio/"

            # Crear la URL completa
            absolute_url = base_url + ruta
            


            mailServer=smtplib.SMTP(setting.EMAIL_HOST, setting.EMAIL_PORT)
            mailServer.starttls()
            mailServer.login(setting.EMAIL_HOST_USER, setting.EMAIL_HOST_PASSWORD)
        
            email_to=user.email
            mensaje=MIMEMultipart()
            mensaje['From']=setting.EMAIL_HOST_USER
            mensaje['To']=email_to
            mensaje['Subject']='Obtención de datos'


            content=render_to_string('alert_email.html', {
                'user':user,
                'informacion':informacion,
                'problemas':problemas,
                'otros':otros,
                'link_home':absolute_url
                
                
            })
            mensaje.attach(MIMEText(content,'html'))
        
            mailServer.sendmail(setting.EMAIL_HOST_USER,email_to,mensaje.as_string())
            print('Correo enviado correctamente')
        
        except Exception as e:
            print('MALO EMAIL')
            data['error']=str(e)
            print(data)
        
        return data


    def save_data(self,data):
        # Comparar data[mac] con el atributo mac de la entidad kit para asignar el id de la vertiente correspondiente
        # Recuperar el ID (Direccion MAC) del mensaje recibido
        if isinstance(data, dict):
            data_mac = data.get("mac", None)
            if not data_mac:
                print("Error: No se encontró la clave 'mac' en los datos recibidos.")
                return
        else:
            print(f"Error: El mensaje recibido no es un diccionario. Valor recibido: {data}")
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

        #Obtiene la comunidad para determinar a los habitantes avisados
        vert_com=vertiente_instance.comunidad
        com_id=int(vert_com.id)
        alerted_user=User.objects.filter(comunidad_id=com_id)
    

        # mostrar cual es el dato que falta
        if not ("caudal" in data):
            print("Falta el caudal")
        if not ("pH" in data): 
            print("Falta el pH")
        if not ("turbiedad" in data):
            print("Falta la turbidez")
        if not ("temperatura" in data):
            print("Falta la temperatura")
        if not ("humedad" in data):
            print("Falta la humedad")
        if not ("mac" in data):
            print("Falta la MAC")

        print("Datos válidos")



        #Se asignan variables a utilizar como apoyo.
        dict_problemas={}
        problema=0

        caudal=data["caudal"]
        caudal_str=str(caudal)
        pH=data["pH"]
        pH_str=str(pH)
        conductividad=data["conductividad"]
        conductividad_str=str(conductividad)
        turbiedad=data["turbiedad"]
        turbiedad_str=str(turbiedad)
        temperatura=data["temperatura"]
        temperatura_str=str(temperatura)
        humedad=data["humedad"]
        humedad_str=str(humedad)

        

        #Revisión y almacenaje de problemas en dict_problemas
        if caudal>700:
            dict_problemas['Caudal']=caudal_str+' L/m'+'  ( El caudal debe tener un flujo menor a 700 L/m )'
            problema=problema+1
        if pH<6 or pH>8.5:
            dict_problemas['pH']=pH_str+' pH'+'  ( El pH debe encontrarse dentro del rango 6-8.5 )'
            problema=problema+1
        if conductividad>1500:
            dict_problemas['Conductividad']=conductividad_str+' µS/cm'+'  ( La conductividad debe ser menor a 1500 µS/cm )'
            problema=problema+1
        if turbiedad>5:
            dict_problemas['Turbiedad']=turbiedad_str+' NTU'+'  ( La turbiedad debe ser igual o menor a 5 NTU )'
            problema=problema+1
        if temperatura<20 or temperatura>30:
            dict_problemas['Temperatura']=temperatura_str+' °C'+'  ( La temperatura debe estar dentro del rango de 20-30°C )'
            problema=problema+1
        if humedad>60:
            dict_problemas['Humedad']=humedad_str+' %'+'  ( La humedad debe ser menor o igual al 60 % )'
            problema=problema+1
        

        #Revisión de problemas
        if problema>=1:
            #Se guardan todos los datos recopilados
            informacion={
            'Caudal':caudal_str+' L/m',
            'pH':pH_str+' pH',
            'Conductividad':conductividad_str+' µS/cm',
            'Turbiedad':turbiedad_str+' NTU',
            'Temperatura':temperatura_str+' °C',
            'Humedad':humedad_str+' %'
            }

            #Se guardan el nombre de la vertiente analizada
            vert_nombre=vertiente_instance.nombre
            otros={
                'vertiente_nombre':vert_nombre
            }
        

            #Se envian correos a todos los habitantes de la comunidad con la vertiente en problemas
            for user_advice in alerted_user:
                self.send_email(user_advice, informacion,dict_problemas, otros)


        ultimo_id = datos.objects.all().aggregate(models.Max('id'))['id__max']
        

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

        dato.id=ultimo_id+1
        dato.save()
        print("Datos guardados exitosamente")


    # Función callback que se llama cuando el cliente recibe un mensaje del broker
    def on_message(self, client, userdata, msg):
        print("Mensaje recibido")
        
        # Decodificar el mensaje
        payload_str = msg.payload.decode().strip()  # Se usa strip() para eliminar espacios en blanco
        
        # Si el mensaje está vacío, imprimir mensaje y finalizar la función
        if not payload_str:
            print("El último mensaje recibido está vacío.")
            print("No se guardará ningún dato.")
            return

        try:
            # Intenta convertir la cadena a un diccionario
            message_dict = json.loads(payload_str)
            
            # Guardar los datos que llegan en el modelo datos
            # Llamar a la función save_data
            self.save_data(message_dict)

        except json.JSONDecodeError:
            # Si hay un error, simplemente usa la cadena tal como está
            message_dict = {"message": payload_str}
            print("Error al decodificar el mensaje")
        
        # Agregar el diccionario a la cola
        message_queue.put(message_dict)
