from django.shortcuts import render
from django.http import HttpResponseRedirect
from application.models import Projet, Plante as ModelPlante, Utilisateur
from application.forms.plante import Plante, ChoixPlante
from application import utilisateurPhotoProfile

def plante(request, projet, formulaire=None):
	pseudo=request.session['pseudo']
	projet=Projet.objects.get(id=projet, plante__isnull=True)
	if projet:
		if not formulaire:
			formulaire=Plante({})
		liste=ModelPlante.objects.all() | Utilisateur.objects.get(pseudo=pseudo).plante.all()
		photo=utilisateurPhotoProfile(Utilisateur.objects.filter(pseudo=pseudo).first().photo)
		return render(request, 'plante.html', {'form': formulaire, 'pseudo': pseudo, 'projet': projet.id,'list' : liste, 'photo': photo, 'existe': liste.exists()})
	return HttpResponseRedirect('/application/mes-projets/%d/' % projet.id)

def valider_plante(request, projet):
	if request.method=='POST':
		pseudo=request.session['pseudo']
		formulaire=Plante(request.POST)
		if formulaire.is_valid():
			formulaire.enregistrer(projet=projet, pseudo=pseudo)
			return HttpResponseRedirect('/application/mes-projets/%s/' % projet)
		return plante(request=request, projet=projet, formulaire=formulaire)
	return HttpResponseRedirect('/application/mes-projets/')

def choix_plante(request, projet, formulaire=None):
	if Projet.objects.filter(id=projet, plante__isnull=True).exists():
		pseudo=request.session['pseudo']
		liste=ModelPlante.objects.all() | Utilisateur.objects.get(pseudo=pseudo).plante.all()
		if liste.exists():
			if not formulaire:
				formulaire=ChoixPlante({})
			photo=utilisateurPhotoProfile(Utilisateur.objects.filter(pseudo=pseudo).first().photo)
			return render(request, 'choix_plante.html', {'form': formulaire, 'pseudo': pseudo, 'projet': projet,'list' : liste, 'photo': photo})
		return HttpResponseRedirect('/application/%s/plante/' % projet)
	return HttpResponseRedirect('/application/mes-projets/%s/' % projet)

def valider_choix_plante(request, projet):
	if request.method=='POST':
		pseudo=request.session['pseudo']
		formulaire=ChoixPlante(request.POST)
		if formulaire.is_valid():
			formulaire.enregistrer(projet=projet, pseudo=pseudo)
			return HttpResponseRedirect('/application/mes-projets/%s/' % projet)
		return choix_plante(request=request, projet=projet, formulaire=formulaire)
	return HttpResponseRedirect('/application/mes-projets/')
