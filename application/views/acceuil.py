from application.forms.connexion import Connexion
from django.http import HttpResponseRedirect 
from application.forms.contact import Email
from django.shortcuts import render

def index(request):
	return render(request, 'acceuil.html', {'form': Email({})})

def connexion(request):
	return render(request, 'connexion.html', {'form' : Connexion({})})

def valider(request):
	if request.method=='POST':
		connexion=Connexion(request.POST)
		if connexion.is_valid():
			request.session['pseudo']=connexion.get('pseudo')
			request.session['mot_de_passe']=connexion.get('mot_de_passe')
			return HttpResponseRedirect('/application/mes-projets/')
		return render(request, 'connexion.html', {'form' : connexion})
	return HttpResponseRedirect('/application/connexion/')

def deconnexion(request):
	del request.session['pseudo']
	del request.session['mot_de_passe']
	return HttpResponseRedirect('/application/')

def envoyer_message(request):
	if request.method=="POST":
		formulaire=Email(request.POST)
		if formulaire.is_valid():
			formulaire.envoyer_message()
		else:
			return render(request, 'acceuil.html', {'form': formulaire})
	return HttpResponseRedirect('/application/')
