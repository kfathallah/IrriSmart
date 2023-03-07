from django.http import HttpResponseRedirect
from django.shortcuts import render
from application.forms.inscription import Inscription
import md5

def index(request):
	return render(request, 'formulaire.html', {'form' : Inscription({})})

def valider(request):
	if request.method=='POST':
		formulaire=Inscription(request.POST, request.FILES)
		if formulaire.is_valid():
			request.session['pseudo']=formulaire.get('pseudo')
			request.session['mot_de_passe']=formulaire.get('mot_de_passe')
			formulaire.enregistrer()
			return HttpResponseRedirect('/application/mes-projets/')
		return render(request, 'formulaire.html', {'form' : formulaire})
	return HttpResponseRedirect('/application/Inscription/')
