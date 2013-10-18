# Django settings for hyton project.
from settings_default import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy',
    }
}

BROKER_URL = 'redis://localhost:6379/0'
CELERY_DEFAULT_QUEUE = 'deartota'

BROKER_URL = 'redis://localhost:6379/0'
PUBSUB_URL = 'redis://localhost:6379/1'
RPC_SERVER = 'tcp://0.0.0.0:4242'

SOCKET_SERVER = 'http://localhost:9000'
import djcelery
djcelery.setup_loader()

from mongoengine import connect
connect('deartota')
