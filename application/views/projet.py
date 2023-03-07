from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from application.models import Projet, Utilisateur, Polygone, Noeud
from application.forms.projet import Projet as CreationProjet
from application.projet import Projet as Formulaire, getDonnees
from application import as_geojson, utilisateurPhotoProfile
from ast import literal_eval

def index(request):
	pseudo=request.session['pseudo']
	photo=utilisateurPhotoProfile(Utilisateur.objects.filter(pseudo=pseudo).first().photo)
	projets=Projet.objects.filter(utilisateur__pseudo=pseudo)
	return render(request, 'mes_projets.html', {'photo': photo, 'pseudo': pseudo, 'list': projets})

def projet(request, projet):
	projet=Projet.objects.get(utilisateur__pseudo=request.session['pseudo'], id=projet)
	if projet:
		noeuds=Noeud.objects.filter(projet=projet.id)
		polygones=projet.polygone.all()
		if projet.type!='P' and not polygones.exists():
			return HttpResponseRedirect('/application/%d/parcelle/' % projet.id)
		if not projet.plante:
			return HttpResponseRedirect('/application/%d/choix-plante/' % projet.id)
		if not projet.sol:
			return HttpResponseRedirect('/application/%d/choix-sol/' % projet.id)
		if projet.type!='O' and not noeuds.exists():
			return HttpResponseRedirect('/application/%d/noeud/' % projet.id)
		if polygones:
			centre=polygones.first().polygone.centroid
		else:
			centre=noeuds.first().position
		formulaire=Formulaire({'centre': centre, 'nom': projet.nom, 'date': projet.date, 'type_irrigation': projet.type_irrigation, 'type': projet.type, 'plante': projet.plante, 'noeuds': noeuds, 'parcelle': as_geojson(polygones.only('polygone')), 'sol': projet.sol, 'noeud': as_geojson(noeuds), 'id': projet.id})
		formulaire.creer()
		pseudo=request.session['pseudo']
		photo=utilisateurPhotoProfile(Utilisateur.objects.filter(pseudo=pseudo).first().photo)
		return render(request, 'projet.html', {'projet': formulaire, 'photo': photo, 'pseudo': pseudo})
	return HttpResponseRedirect('/application/mes-projets/')

def creation_projet(request):
	pseudo=request.session['pseudo']
	utilisateur=Utilisateur.objects.filter(pseudo=pseudo).first()
	photo=utilisateurPhotoProfile(utilisateur.photo)
	return render(request, 'creation_projet.html', {'form' : CreationProjet({}), 'pseudo': pseudo, 'photo': photo})

def valider_projet(request):
	if request.method=="POST":
		formulaire=CreationProjet(request.POST)
		pseudo=request.session['pseudo']
		if formulaire.is_valid():
			projet=formulaire.enregistrer(pseudo=pseudo)
			return HttpResponseRedirect('/application/mes-projets/%d/' % projet.id)
		photo=utilisateurPhotoProfile(Utilisateur.objects.filter(pseudo=pseudo).first().photo)
		return render(request, "creation_projet.html", {'form': formulaire, 'pseudo': pseudo, 'photo': photo})
	return HttpResponseRedirect('/application/creation-projet/')

def update_donnees(request, projet):
	noeuds_non_actif, donnees=getDonnees(projet=Projet.objects.get(id=projet), graphes=literal_eval(request.POST['graphes']))
	return JsonResponse({'graphe': noeuds_non_actif, 'donnee': donnees}, safe=False)

def supprimer_projet(request, projet):
	Projet.supprimer(id=projet)
	return HttpResponseRedirect('/application/mes-projets/')
