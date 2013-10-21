from django.template import RequestContext
from django.shortcuts import render_to_response
from lineas.documents import Linea
from django.conf import settings
from datetime import datetime, date
import simplejson as json


class DateTimeJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime) or isinstance(obj, date):
            return obj.isoformat()
        else:
            return super(DateTimeJSONEncoder, self).default(obj)


def index(request, t='base.html'):
    lineas = Linea.objects.all()
    # Query latest trains for each line
    lineas = [
        {
            'nombre': l.nombre,
            'estaciones': [
                {
                    'estacion': e,
                    'proximos_destino': [],
                    'proximos_origen': []
                } for e in l.estaciones
            ]
        } for l in lineas
    ]
    return render_to_response(
    	t,
    	{
    		'lineas': DateTimeJSONEncoder().encode(lineas),
            'SOCKET_SERVER': settings.SOCKET_SERVER
    	},
    	RequestContext(request)
    )
