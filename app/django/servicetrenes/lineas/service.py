import urllib2
from lineas.messaging import send_proximo_tren

SERVICE_KEY = 'v%23v%23QTUtWp%23MpWRy80Q0knTE10I30kj%23JNyZ'
SERVICE_RND = 'cqbzhBACphR46LlX&'

import logging
logger = logging.getLogger('trenes')

class ProximoTrenService(object):
    SERVICE_URI = 'http://trenes.mininterior.gov.ar/ajax_arribos.php?ramal=%s&%s'
    html = ''

    def __init__(self, linea):
        self.SERVICE_URI = self.SERVICE_URI % (
            linea.service_id,
            'rnd=%skey=%s' % (SERVICE_RND, SERVICE_KEY)
        )
        self.response = urllib2.urlopen(self.SERVICE_URI).read()
        arr = self.response.split("_")
        try:
            cant = int(arr[0])
            if len(arr) > 0 and cant > 0:
                for estacion in linea.estaciones:
                    try:
                        index = linea.estaciones.index(estacion)
                        d = {
                            'linea': linea.pk,
                            'estacion': index,
                            'proximos_destino': [
                                int(arr[index*6+i]) for i in range(4, 7) if int(arr[index*6+i]) != -1
                            ],
                            'proximos_origen': [
                                int(arr[index*6+i]) for i in range(1, 4) if int(arr[index*6+i]) != -1
                            ]
                        }
                        logger.debug(('sending', d))
                        send_proximo_tren(d)
                    except:
                        pass
        except:
            pass
