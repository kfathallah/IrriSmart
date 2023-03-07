from django.shortcuts import render
from django.http import HttpResponseRedirect
from application.models import Projet, Utilisateur, Sol as ModelSol
from application.forms.sol import ChoixSol, Sol
from application import utilisateurPhotoProfile

def sol(request, projet, formulaire=None):
	projet=Projet.objects.get(id=projet, sol__isnull=True)
	if projet:
		pseudo=request.session['pseudo']
		liste=ModelSol.objects.filter(utilisateur__pseudo=pseudo).all()
		photo=utilisateurPhotoProfile(Utilisateur.objects.filter(pseudo=pseudo).first().photo)
		if not formulaire:
			formulaire=Sol({})
		return render(request, 'sol.html', {'form': formulaire, 'pseudo': pseudo, 'photo': photo, 'projet': projet.id, 'existe': liste.exists()})
	return HttpResponseRedirect('/application/mes-projets/%d/' % projet.id)

def valider_sol(request, projet):
	if request.method=='POST':
		pseudo=request.session['pseudo']
		formulaire=Sol(request.POST)
		if formulaire.is_valid():
			formulaire.enregistrer(projet=projet, pseudo=pseudo)
			return HttpResponseRedirect('/application/mes-projets/%s/' % projet)
		return sol(request=request, projet=projet, formulaire=formulaire)
	return HttpResponseRedirect('/application/mes-projets/')

def choix_sol(request, projet, formulaire=None):
	if Projet.objects.filter(id=projet, sol__isnull=True).exists():
		pseudo=request.session['pseudo']
		liste=ModelSol.objects.filter(utilisateur__pseudo=pseudo).all()
		if liste.exists():
			photo=utilisateurPhotoProfile(Utilisateur.objects.filter(pseudo=pseudo).first().photo)
			if not formulaire:
				formulaire=ChoixSol({})
			return render(request, 'choix_sol.html', {'form': formulaire, 'pseudo': pseudo, 'list': liste, 'photo': photo, 'projet': projet})
		return HttpResponseRedirect('/application/%s/sol/' % projet)
	return HttpResponseRedirect('/application/mes-projets/%s/' % projet)

def valider_choix_sol(request, projet):
	if request.method=='POST':
		pseudo=request.session['pseudo']
		formulaire=ChoixSol(request.POST)
		if formulaire.is_valid():
			formulaire.enregistrer(projet=projet, pseudo=pseudo)
			return HttpResponseRedirect('/application/mes-projets/%s/' % projet)
		return choix_sol(request=request, projet=projet, formulaire=formulaire)
	return HttpResponseRedirect('/application/mes-projets/')
