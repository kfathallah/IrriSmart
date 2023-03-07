from application.models import ClimatNoeud, ClimatOpenWeather, Climat
from application import TYPE_IRRIGATION, TYPE_PROJET
from ast import literal_eval
import datetime

liste=['id', 'date', 'time', 'climatopenweather', 'climatnoeud', 'altitude']

humidite_sol='humidite_sol'

def getIndex(liste, condition):
	for id, valeur in enumerate(liste):
		if valeur['date']==condition:
			return id
	return None

def getDonnees(projet, graphes):
	climat=[]
	noeuds_non_actif=[]
	donnees={}
	for graphe in graphes:
		if graphe['title']=='OpenWeather':
			valeurs=ClimatOpenWeather.objects.filter(projet=projet.id).order_by('-id')[:20]
			climat=climat+list(valeurs)
			liste.append(humidite_sol)
		else:
			valeurs=ClimatNoeud.objects.filter(noeud=graphe['valueField']).order_by('-id')[:20]
			climat=climat+list(valeurs)
			if valeurs.exists():
				first=valeurs.first()
				date=first.date
				heure=first.time
				now=datetime.datetime.now()
				if date!=now.date() or not ((now-datetime.timedelta(minutes=1)).time()<=heure<=now.time()):
					noeuds_non_actif.append(graphe['title'])
	for field in Climat._meta.get_fields():
		if not field.name in liste:
			liste_donnee=[]
			for valeur in reversed(climat):
				donnee={}
				date='%s %s' % (valeur.date, valeur.time)
				id=getIndex(liste=liste_donnee, condition=date)
				if id:
					if type(climat[0])==ClimatOpenWeather:
						liste_donnee[id]['openWeather']=valeur.__dict__[field.name]
					else:
						liste_donnee[id][valeur.noeud.__str__()]=valeur.__dict__[field.name]
				else:
					if type(climat[0])==ClimatOpenWeather:
						donnee['openWeather']=valeur.__dict__[field.name]
					else:
						donnee[valeur.noeud.__str__()]=valeur.__dict__[field.name]
					donnee['date']=date
					liste_donnee.append(donnee)
			donnees[field.name]=liste_donnee
	return noeuds_non_actif, donnees

class Projet():
	def __init__(self, initial):
		self.centre=initial['centre']
		self.id=initial['id']
		self.nom=initial['nom']
		self.date=initial['date']
		self.type_irrigation=dict(TYPE_IRRIGATION)[initial['type_irrigation']]
		self.type_projet=initial['type']
		self.type=dict(TYPE_PROJET)[self.type_projet]
		self.plante=Plante({'plante': initial['plante'], 'date_creation_projet': self.date})
		self.noeuds=initial['noeuds']
		self.noeud=initial['noeud']
		self.parcelle=initial['parcelle']
		self.sol=Sol(sol=initial['sol'])
		self.noeud_id=[]
		self.graphe=[]
		self.donnee={}
		self.noeuds_non_actif=[]
		self.google_map_titre=None

	def setGoogleMapTitre(self):
		noeud={}
		try:
			noeud=literal_eval(self.noeud)
		except ValueError:
			noeud['features']='existe'
		parcelle=literal_eval(self.parcelle)
		if noeud['features'] and parcelle['features']:
			self.google_map_titre='polygones et noeuds'
		elif noeud['features'] and not parcelle['features']:
			self.google_map_titre='noeuds'
		else:
			self.google_map_titre='polygones'

	def setGraphe(self):
		if self.noeuds:
			for noeud in self.noeuds:
				id=noeud.identifiant_arduino.__str__()
				noeud={'id': len(self.noeud_id)+1, 'identifiant': id}
				self.noeud_id.append(noeud)
				self.graphe.append({"balloonText": "[[title]]: [[value]]", "bullet": "round", "id": noeud['id'], "title": "Noeud-%s" % noeud['id'], "type": "smoothedLine", "valueField": id})
		else:
			self.graphe.append({"balloonText": "[[title]]: [[value]]", "bullet": "round", "id": "0", "title": "OpenWeather", "type": "smoothedLine", "valueField": "openWeather"})

	def setDonnee(self):
		climat=[]
		if self.type_projet in ['N', 'P']:
			for noeud in self.noeud_id:
				valeurs=ClimatNoeud.objects.filter(noeud=noeud['identifiant']).order_by('-id')[:20]
				climat=climat+list(valeurs)
				if not valeurs.exists():
					self.noeuds_non_actif.append('Noeud-%d' % noeud['id'])
		else:
			valeurs=ClimatOpenWeather.objects.filter(projet=self.id).order_by('-id')[:20]
			climat=climat+list(valeurs)
			liste.append(humidite_sol)
		for field in Climat._meta.get_fields():
			if not field.name in liste:
				liste_donnee=[]
				for valeur in reversed(climat):
					donnee={}
					date='%s %s' % (valeur.date, valeur.time)
					id=getIndex(liste=liste_donnee, condition=date)
					if id:
						if type(climat[0])==ClimatOpenWeather:
							liste_donnee[id]['openWeather']=valeur.__dict__[field.name]
						else:
							liste_donnee[id][valeur.noeud.identifiant_arduino.__str__()]=valeur.__dict__[field.name]
					else:
						if type(climat[0])==ClimatOpenWeather:
							donnee['openWeather']=valeur.__dict__[field.name.__str__()]
						else:
							donnee[valeur.noeud.identifiant_arduino.__str__()]=valeur.__dict__[field.name]
						donnee['date']=date
						liste_donnee.append(donnee)
				self.donnee[field.name]=liste_donnee

	def creer(self):
		self.setGoogleMapTitre()
		self.setGraphe()
		self.setDonnee()

class Plante():
	def __init__(self, initial):
		plante=initial['plante']
		date_creation_projet=initial['date_creation_projet']
		maintenent=datetime.datetime.now().date()
		phase=self.delais(plante=plante, date=date_creation_projet)
		if phase['initial']>=maintenent:
			self.phase='Initial'
			self.kc=plante.initial_Kc
		elif phase['developpement']>=maintenent:
			self.phase='Developpement'
			self.kc=plante.developpement_Kc
		elif phase['mi-saison']>=maintenent:
			self.phase='Mi-saison'
			self.kc=plante.mi_saison_Kc
		elif phase['recolte']>=maintenent:
			self.phase='Recolte'
			self.kc=plante.recolte_Kc
		else:
			self.phase='Terminer'
			self.kc=0
		self.nom=plante.nom

	def terminer(self):
		return self.kc==0 and self.phase=='Terminer'

	def delais(self, plante, date):
		phase={}
		if plante.par=='J':
			phase['initial']=date+datetime.timedelta(days=plante.initial)
			phase['developpement']=date+datetime.timedelta(days=plante.initial+plante.developpement)
			phase['mi-saison']=date+datetime.timedelta(days=plante.initial+plante.developpement+plante.mi_saison)
			phase['recolte']=date+datetime.timedelta(days=plante.initial+plante.developpement+plante.mi_saison+plante.recolte)
		elif plante.par=='S':
			phase['initial']=date+datetime.timedelta(days=plante.initial*7)
			phase['developpement']=date+datetime.timedelta(days=(plante.initial+plante.developpement)*7)
			phase['mi-saison']=date+datetime.timedelta(days=(plante.initial+plante.developpement+plante.mi_saison)*7)
			phase['recolte']=date+datetime.timedelta(days=(plante.initial+plante.developpement+plante.mi_saison+plante.recolte)*7)
		else:
			phase['initial']=date+datetime.timedelta(months=plante.initial)
			phase['developpement']=date+datetime.timedelta(months=plante.initial+plante.developpement)
			phase['mi-saison']=date+datetime.timedelta(months=plante.initial+plante.developpement+plante.mi_saison)
			phase['recolte']=date+datetime.timedelta(months=plante.initial+plante.developpement+plante.mi_saison+plante.recolte)
		phase['initial']=phase['initial'].date()
		phase['developpement']=phase['developpement'].date()
		phase['mi-saison']=phase['mi-saison'].date()
		phase['recolte']=phase['recolte'].date()
		return phase

class Sol():
	def __init__(self, sol):
		self.type_sol=[
			{'argile': [0, 5], 'liste': [
				{'limon': [0, 10], 'sol': {'titre': 'Terres sableuses', 'K': 0.7}},
				{'limon': [10, 30], 'sol': {'titre': 'Terres sablo-limoneuses', 'K': 1}},
				{'limon': [30, 60], 'sol': {'titre': 'Terres limono-sableuses', 'K': 1.55}},
				{'limon': [60, 100], 'sol': {'titre': 'Terres limoneuses', 'K': 1.8}}
			]},
			{'argile': [5, 12.5], 'liste': [
				{'limon': [0, 10], 'sol': {'titre': 'Terres sablo-argileuses', 'K': 1.4}},
				{'limon': [10, 30], 'sol': {'titre': 'Terres sablo-limono-argileuses', 'K': 1.5}},
				{'limon': [30, 60], 'sol': {'titre': 'Terres limono-sablo-sableuses', 'K': 1.65}},
				{'limon': [60, 100], 'sol': {'titre': 'Terres limono-argileuses', 'K': 2}}
			]},
			{'argile': [12.5, 25], 'liste': [
				{'limon': [0, 10], 'sol': {'titre': 'Terres argilo-sableuses', 'K': 1.7}},
				{'limon': [10, 30], 'sol': {'titre': 'Terres argilo-limoneuses', 'K': 1.5}},
				{'limon': [30, 60], 'sol': {'titre': 'Terres argilo-limono-sableuses', 'K': 1.8}},
				{'limon': [60, 100], 'sol': {'titre': 'Terres argilo-limoneuses', 'K': 2}}
			]},
			{'argile': [25, 40], 'liste': [
				{'limon': [0, 10], 'sol': {'titre': 'Terres argiles sableuses', 'K': 1.7}},
				{'limon': [10, 30], 'sol': {'titre': 'Terres argiles sablo-limoneuses', 'K': 1.8}},
				{'limon': [30, 60], 'sol': {'titre': 'Terres argiles sablo-limoneuses', 'K': 1.8}},
				{'limon': [60, 100], 'sol': {'titre': 'Terres argiles limoneuses', 'K': 1.9}}
			]},
			{'argile': [40, 60], 'liste': [
				{'limon': [0, 60], 'sol': {'titre': 'Terres argileuses', 'K': 1.85}}
			]},
			{'argile': [60, 100], 'liste': [
				{'limon': [0, 40], 'sol': {'titre': 'Terres argileuses lourdes', 'K': 1.9}}
			]}
		]
		temporaire=self.get_K(sol)
		if temporaire:
			self.K=temporaire['K']
			self.type=temporaire['titre']
			self.nom=sol.nom
			self.sable=sol.sable
			self.argile=sol.argile
			self.limon=sol.limon
		else:
			self.K=0
			self.type='Inconnu'
			self.nom='Inconnu'
			self.sable=0
			self.argile=0
			self.limon=0

	def get_K(self, sol):
		for type_sol in self.type_sol:
			min=type_sol['argile'][0]
			max=type_sol['argile'][1]
			if min<=sol.argile<=max:
				for type_sol in type_sol['liste']:
					min=type_sol['limon'][0]
					max=type_sol['limon'][1]
					if min<=sol.limon<=max:
						return type_sol['sol']
		return None
