#!/usr/bin/env python
# import django env
from django.core.management import setup_environ
from servicetrenes import settings
setup_environ(settings)

from lineas.documents import Linea, ProximoTren

import zerorpc

class ZRPCServer(object):
    def lineas(self):
        return [
            {
                'id': str(l.id),
                'nombre': l.nombre,
            }
            for l in Linea.objects.all()
        ]

    def estaciones(self, linea):
        try:
            l = Linea.objects.get(id=linea)
            return l.estaciones
        except:
            return {
                'error': 'No existe linea con id %s' % linea
            }

    def proximos_trenes(self, linea, estacion):
        try:
            l = Linea.objects.get(id=linea)
            pts = ProximoTren.objects.filter(
                linea=l,
                _estacion=int(estacion)
            )
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
s.bind(settings.RPC_SERVER)
s.run()
