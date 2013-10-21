from django.template import RequestContext
from django.shortcuts import render_to_response
from lineas.documents import Linea, ProximoTren
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
    lineas = [
        {
            'instance': l,
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
    for i in range(len(lineas)):
        l = lineas[i]
        for j in range(len(l['estaciones'])):
            pts = ProximoTren.objects.filter(
                linea=l['instance'],
                _estacion=int(j)
            )
            if pts.count():
                l['estaciones'][j]['proximos_destino'] = pts[0].proximos_destino
                l['estaciones'][j]['proximos_origen'] = pts[0].proximos_origen
        l.pop('instance', None)
        lineas[i] = l
    return render_to_response(
    	t,
    	{
    		'lineas': DateTimeJSONEncoder().encode(lineas),
            'SOCKET_SERVER': settings.SOCKET_SERVER
    	},
    	RequestContext(request)
    )
