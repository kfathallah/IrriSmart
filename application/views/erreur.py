from application import utilisateurPhotoProfile
from django.template import Context, loader
from application.models import Utilisateur
from django.http import HttpResponse
from django.shortcuts import render

def erreur(request, code, message):
	pseudo=request.session['pseudo']
	utilisateur=Utilisateur.objects.get(pseudo=pseudo)
	photo=utilisateurPhotoProfile(photo=utilisateur.photo)
	template=loader.get_template('erreur.html')
	context=Context({'code': code, 'message': message, 'pseudo': pseudo, 'photo': photo})
	return HttpResponse(content=template.render(context), content_type='text/html; charset=utf-8', status=code)

def erreur404(request):
	return erreur(request=request, code=404, message='Oops, Cette page est Introuvable')

def erreur500(request):
	return erreur(request=request, code=500, message='Oops, Cette page est Introuvable')
