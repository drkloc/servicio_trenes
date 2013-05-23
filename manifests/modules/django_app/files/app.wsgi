import os, sys, site

from django.core.handlers.wsgi import WSGIHandler

site.addsitedir(
    '/opt/apps/trenes/stream_n_rpc/lib/python2.7/site-packages/'
)
activate_this = os.path.expanduser(
    "/opt/apps/trenes/stream_n_rpc/bin/activate_this.py"
)
execfile(activate_this, dict(__file__=activate_this))

project = '/opt/apps/trenes/stream_n_rpc/servicio_trenes'
workspace = os.path.dirname(project)
sys.path.append(workspace)

os.environ['DJANGO_SETTINGS_MODULE'] = 'servicio_trenes.settings'
application = WSGIHandler()
