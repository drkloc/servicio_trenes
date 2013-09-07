from celery.task import PeriodicTask
from datetime import timedelta
from lineas.messaging import process_proximos_trenes


class GetProximosTrenesTask(PeriodicTask):
    run_every = timedelta(seconds=10)

    def run(self, **kwargs):
        from lineas.documents import Linea
        from lineas.service import ProximoTrenService
        for linea in Linea.objects.all():
            ProximoTrenService(linea)


class ProcessProximosTrenesTask(PeriodicTask):
    run_every = timedelta(seconds=20)

    def run(self, **kwargs):
        process_proximos_trenes()
