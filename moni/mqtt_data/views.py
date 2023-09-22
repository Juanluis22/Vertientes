from django.shortcuts import render
from .middleware import message_queue
from django.http import StreamingHttpResponse
import json


def data(request):
    def event_stream():
        while True:
            message_dict = message_queue.get()
            compact_message = json.dumps(message_dict)
            yield f"data: {compact_message}\n\n"

    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')



def display(request):
    return render(request, 'mqtt_data.html')
