from django.http import HttpResponseRedirect, JsonResponse
from application import utilisateurPhotoProfile
from application.forms.mot_de_passe import Mdp
from application.forms.profile import Profile
from application.models import Utilisateur
from application.forms.photo import Photo
from django.shortcuts import render
import md5

def index(request, formulaire=None):
	pseudo=request.session['pseudo']
	utilisateur=Utilisateur.objects.get(pseudo=pseudo)
	photo=utilisateurPhotoProfile(Utilisateur.objects.get(pseudo=pseudo).photo)
	if not formulaire:
		data={}
		data['nom']=utilisateur.nom
		data['prenom']=utilisateur.prenom
		data['email']=utilisateur.email
		data['adresse']=utilisateur.adresse
		data['latitude']=utilisateur.position.y
		data['longitude']=utilisateur.position.x
		data['telephone']=utilisateur.telephone
		data['pseudo']=utilisateur.pseudo
		formulaire=Profile(data)
	return render(request, 'profile.html', {'photo': photo, 'pseudo': pseudo, 'form': formulaire})

def valider(request):
	if request.method=='POST':
		formulaire=Profile(request.POST, request.FILES)
		pseudo=request.session['pseudo']
		if formulaire.is_valid():
			formulaire.enregistrer(pseudo=pseudo)
			return HttpResponseRedirect('/application/mes-projets/')
		return index(request=request, formulaire=formulaire)
	return HttpResponseRedirect('/application/mon-profile/')

def supprimer_photo(request):
	if request.method=='POST' and request.is_ajax():
		donnee={'terminer': False}
		pseudo=request.POST['pseudo']
		Utilisateur.supprimer_photo(pseudo=pseudo)
		donnee['terminer']=True
		return JsonResponse(donnee)

def photo(request, formulaire=None):
	pseudo=request.session['pseudo']
	photo_profile=Utilisateur.objects.get(pseudo=pseudo).photo
	photo=utilisateurPhotoProfile(photo_profile)
	if not formulaire:
		formulaire=Photo({})
	return render(request, 'photo.html', {'photo': photo, 'pseudo': pseudo, 'form': formulaire, 'photo_profile': photo_profile})

def valider_photo(request):
	if request.method=='POST':
		pseudo=request.session['pseudo']
		formulaire=Photo(request.FILES, request.POST)
		if formulaire.is_valid():
			formulaire.enregistrer(pseudo=pseudo)
			return HttpResponseRedirect('/application/mes-projets/')
		return photo(request=request, formulaire=formulaire)
	return HttpResponseRedirect('/application/profile/photo/')

def mot_de_passe(request, formulaire=None):
	pseudo=request.session['pseudo']
	photo_profile=Utilisateur.objects.get(pseudo=pseudo).photo
	photo=utilisateurPhotoProfile(photo_profile)
	if not formulaire:
		formulaire=Mdp({})
	return render(request, 'mot_de_passe.html', {'photo': photo, 'pseudo': pseudo, 'form' : formulaire, 'photo_profile': photo_profile})

def valider_mot_de_passe(request):
	if request.method=='POST':
		pseudo=request.session['pseudo']
		formulaire=Mdp(request.POST)
		if formulaire.is_valid(pseudo=pseudo):
			request.session['mot_de_passe']=formulaire.enregistrer(pseudo=pseudo)
			return HttpResponseRedirect('/application/mes-projets/')
		return mot_de_passe(request=request, formulaire=formulaire)
	return HttpResponseRedirect('/application/profile/mot-de-passe/')
