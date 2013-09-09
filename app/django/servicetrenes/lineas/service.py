import httplib2
from lineas.messaging import send_proximo_tren

SERVICE_KEY = 'v%23v%23QTUtWp%23MpWRy80Q0knTE10I30kj%23JNyZ'
SERVICE_RND = 'cqbzhBACphR46LlX'

import logging
logger = logging.getLogger('trenes')

class ProximoTrenService(object):
    SERVICE_URI = 'http://trenes.mininterior.gov.ar/ajax_arribos.php?ramal=%s&%s'
    html = ''

    def __init__(self, linea):
        self.SERVICE_URI = self.SERVICE_URI % (
            linea.service_id,
            'rnd=%s&key=%s' % (SERVICE_RND, SERVICE_KEY)
        )
        try:
            h = httplib2.Http(".cache")
            headers, self.response = h.request(self.SERVICE_URI)
            if headers['status'] == "200":
                arr = self.response.split("_")
                try:
                    cant = int(arr[0]) if len(arr) else 0
                    if cant > 0:
                        for estacion in linea.estaciones:
                            try:
                                index = linea.estaciones.index(estacion)
                                d = {
                                    'linea': str(linea.id),
                                    'estacion': index,
                                    'proximos_destino': [
                                        int(arr[index*6+i]) for i in range(4, 7) if int(arr[index*6+i]) != -1
                                    ],
                                    'proximos_origen': [
                                        int(arr[index*6+i]) for i in range(1, 4) if int(arr[index*6+i]) != -1
                                    ]
                                }
                                send_proximo_tren(d)
                            except Exception as e:
                                logger.debug('%s - %s - %s' % (str(e), arr, linea.service_id))
                except Exception as e:
                    logger.debug('%s -- %s -- %s' % (str(e),arr, linea.service_id))
            else:
                logger.debug(headers)
        except Exception as e:
            logger.debug('%s --- %s --- %s' % (str(e), arr, linea.service_id))
