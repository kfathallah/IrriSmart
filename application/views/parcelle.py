from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from application import utilisateurPhotoProfile, as_geojson
from application.models import Projet, Utilisateur, Polygone
from ast import literal_eval

def index(request, projet):
	pseudo=request.session['pseudo']
	resultat=Projet.objects.get(utilisateur__pseudo=pseudo, id=projet)
	if not resultat.polygone.exists() and resultat.type!='P':
		utilisateur=Utilisateur.objects.get(pseudo=pseudo)
		photo=utilisateurPhotoProfile(utilisateur.photo)
		projets=Projet.objects.filter(utilisateur__pseudo=pseudo, type='O', plante__isnull=False, sol__isnull=False, polygone__isnull=False, noeud__isnull=True).distinct() | Projet.objects.filter(utilisateur__pseudo=pseudo, type='N', plante__isnull=False, sol__isnull=False, polygone__isnull=False, noeud__isnull=False).distinct()
		latitude=utilisateur.position.y
		longitude=utilisateur.position.x
		return render(request, 'parcelle.html', {'photo': photo, 'pseudo': pseudo, 'projets': projets, 'projet': projet, 'latitude': latitude, 'longitude': longitude})
	return HttpResponseRedirect('/application/mes-projets/%s/' % projet)

def valider_parcelle(request, projet):
	if request.method=="POST" and request.is_ajax():
		geojson=literal_eval(request.POST['geojson'])
		pseudo=request.session['pseudo']
		Projet.add_polygones(projet_id=projet, geojson=geojson)
		return JsonResponse('/application/mes-projets/%s/' % projet, safe=False)
	return JsonResponse('/application/creation-projet/')

def importer_polygone(request):
	if request.method=='POST' and request.is_ajax() and 'id[]' in request.POST:
		projets_id=request.POST.getlist('id[]')
		list_id=[literal_eval(valeur) for valeur in projets_id]
		polygones=Polygone.objects.filter(projet__in=list_id)
		geojson=as_geojson(polygones)
		return JsonResponse(geojson, content_type="application/json", safe=False)
	return JsonResponse("erreur", safe=False)
