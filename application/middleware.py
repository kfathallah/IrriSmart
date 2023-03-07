from serveur.urls import urls_accessibles, urls_utilisateur_inaccessibles
from application.models import Utilisateur, Projet
from django.http import HttpResponseRedirect
from application import to_integer

class Controlleur(object):
	def __init__(self, get_response):
		self.get_response=get_response
		print("MIDDLEWARE [Controlleur]: %s" % get_response)

	def __call__(self, request):
		current_url=request.get_full_path().__str__()
		liste_valeurs=current_url.split('/')
		if current_url is '/':
			return HttpResponseRedirect('/application/')
		elif liste_valeurs[-2]=='update-donnees':
			print("MISE A JOUR -> %s" % current_url)
			return self.get_response(request)
		elif 'pseudo' in request.session and 'mot_de_passe' in request.session:
			print("CLIENT -> %s" % current_url)
			pseudo=request.session['pseudo']
			mot_de_passe=request.session['mot_de_passe']
			if Utilisateur.exists(pseudo=pseudo, mot_de_passe=mot_de_passe):
				if current_url not in urls_utilisateur_inaccessibles:
					projet=to_integer(liste_valeurs[2])
					if not projet and len(liste_valeurs)>=5:
						projet=to_integer(liste_valeurs[3])
					if projet:
						if not Projet.objects.filter(utilisateur__pseudo=pseudo, id=projet).exists():
							return HttpResponseRedirect('/application/mes-projets/')
					return self.get_response(request)
				return HttpResponseRedirect('/application/mes-projets/')
			del request.session['pseudo']
			del request.session['mot_de_passe']
		elif current_url in urls_accessibles:
			print("REQUEST -> %s" % current_url)
			return self.get_response(request)
		elif current_url.split('/')[1]=='admin':
			print("ADMIN REQUEST -> %s" % current_url)
			return self.get_response(request)
		return HttpResponseRedirect('/application/')
