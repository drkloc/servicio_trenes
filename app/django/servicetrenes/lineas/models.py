from django.db import models
from django.utils.translation import ugettext_lazy as _
from djangotoolbox.fields import ListField

from datetime import datetime


class Linea(models.Model):
    nombre = models.CharField(max_length=255, verbose_name=_('Nombre'))
    service_id = models.IntegerField(unique=True)
    estaciones = ListField()

    class Meta:
        verbose_name = _('Linea')
        verbose_name_plural = _('Lineas')

    def __unicode__(self):
        return u'%s' % self.nombre


class ProximoTren(models.Model):
    linea = models.ForeignKey(
        'Linea',
        related_name='proximos',
        verbose_name=_('Proximo Tren')
    )
    _estacion = models.IntegerField(verbose_name=_('Estacion'))
    proximos_origen = ListField()
    proximos_destino = ListField()
    created = models.DateTimeField(editable=False, verbose_name=_('Fecha de creacion'))

    @property
    def estacion(self):
        return self.linea.estaciones[self._estacion]

    class MongoMeta:
        capped = True
        collection_size = 50 * 1024 * 1024

    def save(self):
        if not self.created:
            self.created = datetime.now()
        super(ProximoTren, self).save()

    def __unicode__(self):
        return u'(%s) %s | %s: %s %s: %s' % (
            self.created,
            self.estacion,
            self.linea.estaciones[0],
            ', '.join(['%s mins' % p for p in self.proximos_origen]),
            self.linea.estaciones[-1],
            ', '.join(['%s mins' % p for p in self.proximos_destino])
        )
