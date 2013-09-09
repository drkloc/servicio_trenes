from celery.messaging import establish_connection
from kombu.compat import Publisher, Consumer
from core.utils import get_redis_client

import json

import logging
from datetime import datetime

logger = logging.getLogger('trenes')


def send_proximo_tren(d):
    connection = establish_connection()
    publisher = Publisher(
        connection=connection,
        exchange="proximos_trenes",
        routing_key="save_proximos_trenes",
        exchange_type="direct"
    )
    publisher.send(d)
    publisher.close()
    connection.close()


def process_proximos_trenes():
    from lineas.documents import Linea, ProximoTren
    connection = establish_connection()
    consumer = Consumer(
        connection=connection,
        queue="proximos_trenes",
        exchange="proximos_trenes",
        routing_key="save_proximos_trenes",
        exchange_type="direct"
    )
    before = datetime.now()
    for message in consumer.iterqueue():
        d = json.loads(message.body)
        try:
            pt = ProximoTren()
            pt.linea = Linea.objects.get(id=d['linea'])
            pt._estacion = d['estacion']
            pt.proximos_origen = d['proximos_origen']
            pt.proximos_destino = d['proximos_destino']
            pt.save()
        except Exception as e:
            logger.debug(d, e)
        message.ack()
    pts = ProximoTren.objects.filter(created__gt=before).order_by('-id')
    pts = [
        {
            'linea': pt.linea.nombre,
            'estacion': pt.estacion,
            'proximos_origen': pt.proximos_origen,
            'proximos_destino': pt.proximos_destino,
        }
        for pt in pts
    ]
    r = get_redis_client()
    r.publish(
        'proximos-trenes',
        pts
    )
    consumer.close()
    connection.close()
