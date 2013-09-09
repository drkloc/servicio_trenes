from django.core.management.base import BaseCommand

from lineas.documents import Linea

LINEAS = {
    'sarmiento': {
        'id': 1,
        'estaciones': [
            'Once', 'Caballito', 'Flores', 'Floresta', 'Villa Luro',
            'Liniers', 'Ciudadela', 'Ramos Mejia', 'Haedo', 'Moron', 'Castelar',
            'Ituzaingo', 'Padua', 'Merlo', 'Paso del Rey', 'Moreno'
        ]
    },
    'mitre_tigre': {
        'id': 5,
        'estaciones': [
            'Retiro', 'Lisandro de la Torre', 'Belgrando', 'Nunez', 'Rivadavia',
            'Vicente Lopez', 'Olivos', 'La Lucila', 'Martinez', 'Acasusso',
            'San Isidro', 'Beccar', 'Victoria', 'Virreyes', 'San Fernando',
            'Carupa', 'Tigre'
        ]
    },
    'mitre_mitre': {
        'id': 7,
        'estaciones': [
            'Retiro', '3 de Febrero', 'Ministro Carranza', 'Colegiales',
            'Belgrano R', 'Coghlan', 'Saavedra', 'Juan B. Justo', 'Florida',
            'Doctor Cetrangolo', 'Mitre'
        ]
    },
    'mitre_suarez': {
        'id': 9,
        'estaciones': [
            'Retiro', '3 de Febrero', 'Ministro Carranza', 'Colegiales',
            'Belgrano R', 'L.M. Drago', 'General Urquiza', 'Pueyrredon',
            'Miguelete', 'San Martin', 'San Andres', 'Malaver',
            'Villa Ballester', 'Chilavert', 'Jose Leon Suarez',
        ]
    },
}


class Command(BaseCommand):
    help='Crea las lineas y sus respectivas estaciones en db'

    def handle(self,*args,**options):
        lineas_in_db = [
            l.service_id for l in Linea.objects.all()
        ]
        for linea in LINEAS:
            service_id = LINEAS[linea]['id']
            estaciones = LINEAS[linea]['estaciones']
            if not (service_id in lineas_in_db):
                l = Linea()
                l.nombre = linea
                l.service_id = service_id
                l.estaciones = estaciones
                l.save()
