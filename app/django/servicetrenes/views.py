from django.template import RequestContext
from django.shortcuts import render_to_response


def index(request, t='base.html'):
    return render_to_response(t, {}, RequestContext(request))
