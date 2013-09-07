#!/usr/bin/env python
# import django env
from django.core.management import setup_environ
import settings
setup_environ(settings)

from datetime import datetime, timedelta
from lineas.documents import Linea, ProximoTren

import zerorpc

DATA_NOT_OLDER_THAN = 45

class ZRPCServer(object):
    def lineas(self):
        return [
            {
                'id': l.id,
                'nombre': l.nombre,
            }
            for l in Linea.objects.all()
        ]

    def estaciones(self, linea):
        try:
            l = Linea.objects.get(pk=linea)
            return l.estaciones
        except:
            return {
                'error': 'No existe linea con id %s' % linea
            }

    def proximos_trenes(self, linea, estacion):
        try:
            l = Linea.objects.get(pk=linea)
            pts = ProximoTren.objects.filter(
                linea=l,
                _estacion=int(estacion),
                created__gt=datetime.now()-timedelta(seconds=DATA_NOT_OLDER_THAN)
            ).order_by('-id')
            if pts.count():
                pts = pts[0]
                return [
                    {
                        'sentido': l.estaciones[0],
                        'proximos_trenes': pts.proximos_origen
                    },
                    {
                        'sentido': l.estaciones[-1],
                        'proximos_trenes': pts.proximos_destino
                    }
                ]
            else:
                return 'No data available'
        except Exception as e:
            return {
                'error': '%s' % e,
            }


s = zerorpc.Server(ZRPCServer())
s.bind("tcp://0.0.0.0:4242")
s.run()
