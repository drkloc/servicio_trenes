from django.conf import settings
from redis import Redis


def get_redis_client():
    r = settings.PUBSUB_URL.replace('redis://', '')
    r = r.replace('/', ':')
    (host, port, db) = r.split(':')
    port = int(port)
    db = int(db)
    r = Redis(host, port, db)
    return r
