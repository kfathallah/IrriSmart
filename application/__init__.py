from serveur.settings import STATIC_URL, MEDIA_URL
from django.db.models.functions import Coalesce
from django.core.serializers import serialize
from django.db.models import Avg
import hashlib
import urllib
import json
import os

TYPE_IRRIGATION=[
	("A", "Irrigation par aspersion"),
	("G", "Techniques d'irrigation gravitaire"),
	("M", "Irrigation localisee et micro-irrigation par le systeme du goutte-a-goutte")
]
TYPE_PROJET=[
	("O", "OpenWeather"),
	("N", "Parcelle"),
	("P", "Plante")
]

def to_float(string):
	try:
		return float(string)
	except ValueError:
		return None

def as_geojson(queryset):
	return serialize('geojson', queryset)

def utilisateurPhotoProfile(photo):
	if photo:
		return "%s%s" %(MEDIA_URL, photo)
	return "%simages/person.png" % STATIC_URL

def mot_de_passe_hash(valeur):
	mot_de_passe_hash=hashlib.md5()
	mot_de_passe_hash.update(valeur.encode('utf-8'))
	return mot_de_passe_hash.hexdigest()

def set_utilisateur_nom(instance, filename):
	extension=filename.split('.')[-1]
	filename="%s.%s" % (instance.pseudo, extension)
	return os.path.join('application', filename)

def to_integer(string):
	try:
		return int(string)
	except ValueError:
		return None

def get_altitude(latitude, longitude):
	apikey="AIzaSyDB__9ljeKo2BWkqUv6mahxdIbDgSI8qmY"
	url="https://maps.googleapis.com/maps/api/elevation/json"
	request=urllib.urlopen(url+"?locations="+str(latitude)+","+str(longitude)+"&key="+apikey)
	try:
		results=json.load(request).get('results')
		if 0<len(results):
			altitude=results[0].get('elevation')
			return altitude
		else:
			print 'HTTP GET Request a echoue.'
	except ValueError, e:
		print 'JSON decode a echoue: '+str(request)
	return None

def calculer_quantite_eau_dans_parcelle(parcelles, humidite_sol, sol):
	somme=0
	for parcelle in parcelles:
		somme+=parcelle.polygone.area
	return sol*somme*humidite_sol

def calculer_quantite(projet, Eto, humidite_sol, plante, sol):
	quantite=Eto*plante.kc
	if not projet.type=='O':
		if quantite!=0:
			quantite-=calculer_quantite_eau_dans_parcelle(parcelles=projet.polygone.all(), humidite_sol=humidite_sol, sol=sol)
		return {'nom': "Quantite d'eau", 'valeur': quantite}
	return {'nom': 'Eto', 'valeur': quantite}

def get_latitude_moy_longitude_moy_altitude_moy(objets, type):
	if objets.exists():
		latitude_somme=0
		longitude_somme=0
		nombre=objets.count()
		if type=='O':
			for objet in objets:
				latitude_somme+=objet.polygone.centroid.y
				longitude_somme+=objet.polygone.centroid.x
		else:
			for objet in objets:
				latitude_somme+=objet.position.y
				longitude_somme+=objet.position.x
		latitude_moy=latitude_somme/nombre
		longitude_moy=longitude_somme/nombre
		altitude_moy=get_altitude(latitude=latitude_moy, longitude=longitude_moy)
		return latitude_moy, longitude_moy, altitude_moy
	return 0, 0, 0
