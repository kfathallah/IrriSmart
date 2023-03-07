from application import get_latitude_moy_longitude_moy_altitude_moy
from application.models import ClimatOpenWeather, Projet
from django.contrib.gis.geos import GEOSGeometry
import schedule
import pyowm
import time

def job():
	projets=Projet.objects.filter(type='O', plante__isnull=False, sol__isnull=False, polygone__isnull=False, noeud__isnull=True)
	nombre=projets.count()
	if nombre!=1:
		print('> Traitement en cours...[%d projets vont etre mis a jour]' % projets.count())
	else:
		print('> Traitement en cours...[1 projet va etre mis a jour]')
	owm=pyowm.OWM('2ef2269947b9572d27f3e1ab95e5223d')
	if owm.is_API_online():
		for projet in projets:
			latitude, longitude, altitude=get_latitude_moy_longitude_moy_altitude_moy(objets=projet.polygone.all(), type='O')
			observation=owm.weather_at_coords(longitude, latitude)
			donnees=observation.get_weather()
			vent=donnees.get_wind()
			humidite=donnees.get_humidity()
			temperature=donnees.get_temperature('celsius')
			nuages=donnees.get_clouds()
			radiation=100-nuages
			pression=donnees.get_pressure()
			climat=ClimatOpenWeather(projet=projet, temperature=temperature['temp'], humidite=humidite, vent=vent['speed'], radiation=radiation, pression=pression['press'])
			climat.save()
			print('    > [nom: "%s"] est a jour.' % projet.nom)
		print('> Traitement termine avec succes.')
	else:
		print('>>> Erreur: API est <Offline>')

print('Planning owm: on')
schedule.every(5).minutes.do(job)
while True:
	schedule.run_pending()
#	time.sleep(550) -> fait du retard
