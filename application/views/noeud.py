from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from application import utilisateurPhotoProfile, as_geojson
from application.models import Projet, Utilisateur, Noeud
import json

def index(request, projet):
	pseudo=request.session['pseudo']
	projet=Projet.objects.get(utilisateur__pseudo=pseudo, id=projet)
	if projet.type!='O' and not Noeud.objects.filter(projet=projet.id).exists():
		utilisateur=Utilisateur.objects.get(pseudo=pseudo)
		photo=utilisateurPhotoProfile(utilisateur.photo)
		latitude=utilisateur.position.y
		longitude=utilisateur.position.x
		parcelles=as_geojson(projet.polygone.all())
		return render(request, 'noeud.html', {'photo': photo, 'pseudo': pseudo, 'latitude': latitude, 'longitude': longitude, 'projet': projet.id, 'parcelles': parcelles})
	return HttpResponseRedirect('/application/mes-projets/%s/' % projet.id)

def valider_noeud(request, projet):
	if request.method=='POST' and request.is_ajax:
		if 'geojson' in request.POST:
			geojson=request.POST['geojson']
			geojson=json.loads(geojson)
			Noeud.create(geojson=geojson, projet=projet)
			return JsonResponse('/application/mes-projets/', safe=False)
		return JsonResponse('/application/mes-projets/%s/' % projet, safe=False)
	return JsonResponse('/application/%s/noeud/' % projet, safe=False)
