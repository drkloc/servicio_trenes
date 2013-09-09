from datetime import datetime
from mongoengine import *


class Linea(Document):
    nombre = StringField(max_length=255)
    service_id = IntField(unique=True)
    estaciones = ListField()
    meta = {
        'indexes': ['nombre', 'service_id']
    }

    @property
    def proximos(self):
        return ProximoTren.objects.filter(linea=self)

    def __unicode__(self):
        return u'%s - %s' % (self.nombre, self.service_id)


class ProximoTren(Document):
    linea = ReferenceField('Linea')
    _estacion = IntField()
    proximos_origen = ListField()
    proximos_destino = ListField()
    created = DateTimeField(default=datetime.now)

    meta = {
        'max_documents': 1000000,
        'max_size': 50 * 1024 * 1024,
        'indexes': ['_estacion', 'created']
    }

    @property
    def estacion(self):
        return self.linea.estaciones[self._estacion]

    def __unicode__(self):
        return u'(%s) %s | %s: %s %s: %s' % (
            self.created,
            self.estacion,
            self.linea.estaciones[0],
            ', '.join(['%s mins' % p for p in self.proximos_origen]),
            self.linea.estaciones[-1],
            ', '.join(['%s mins' % p for p in self.proximos_destino])
        )
