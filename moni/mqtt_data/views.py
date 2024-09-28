from django.shortcuts import render  # Importa la función render para renderizar plantillas
from .middleware import message_queue  # Importa message_queue desde el middleware
from django.http import StreamingHttpResponse  # Importa StreamingHttpResponse para enviar respuestas HTTP en streaming
import json  # Importa el módulo json para trabajar con datos JSON


def data(request):
    """
    Vista que envía datos en tiempo real utilizando Server-Sent Events (SSE).
    """
    def event_stream():
        """
        Generador que obtiene mensajes de la cola y los envía en formato JSON.
        """
        while True:
            message_dict = message_queue.get()  # Obtiene un mensaje de la cola
            compact_message = json.dumps(message_dict)  # Convierte el mensaje a formato JSON
            yield f"data: {compact_message}\n\n"  # Genera el evento SSE con los datos JSON

    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')  # Devuelve una respuesta HTTP en streaming


def display(request):
    """
    Vista que renderiza la plantilla mqtt_data.html.
    """
    return render(request, 'mqtt_data.html')  # Renderiza la plantilla mqtt_data.html