from django.shortcuts import render_to_response
from django.template import RequestContext

def handler404(request):
    response=render_to_response('erreur.html', {'code': 404, 'message': 'Oops, Cette page est Introuvable'}, context_instance=RequestContext(request))
    response.status_code=404
    return response

def handler500(request):
    response=render_to_response('erreur.html', {'code': 500, 'message': 'Un problem dans le serveur'}, context_instance=RequestContext(request))
    response.status_code=500
    return response
