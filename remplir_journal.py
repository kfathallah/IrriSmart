from application.models import ClimatNoeud, ClimatJournaliere, Noeud, ClimatOpenWeather, Projet
from application import calculer_quantite, get_latitude_moy_longitude_moy_altitude_moy
from django.db.models.functions import Coalesce
from email.MIMEMultipart import MIMEMultipart
from application.projet import Sol, Plante
from django.db.models import Max, Min, Avg
from email.MIMEText import MIMEText
import datetime
import schedule
import smtplib
import pyeto
import time
import re

def job():
	date_courrant=datetime.datetime.now().date()
	day_of_year=date_courrant.month*date_courrant.day
	print('Traitement en cours...')
	#>>> Noeuds
	print('    > Traitement des noeuds:')
	noeuds=Noeud.objects.all()
	for noeud in noeuds:
		print('        > Traitement des donnees de [noeud: %s, projet: %s]' % (noeud.identifiant_arduino.__str__(), noeud.projet.nom))
		climats=ClimatNoeud.objects.filter(noeud=noeud)
		if climats.exists():
			climat=climats.aggregate(temperature_moy=Coalesce(Avg('temperature'), 0), temperature_max=Coalesce(Max('temperature'), 0), temperature_min=Coalesce(Min('temperature'), 0), vent_moy=Coalesce(Avg('vent'), 0), vent_max=Coalesce(Max('vent'), 0), vent_min=Coalesce(Min('vent'), 0), radiation_moy=Coalesce(Avg('radiation'), 0), radiation_max=Coalesce(Max('radiation'), 0), radiation_min=Coalesce(Min('radiation'), 0), pression_moy=Coalesce(Avg('pression'), 0), pression_max=Coalesce(Max('pression'), 0), pression_min=Coalesce(Min('pression'), 0), humidite_moy=Coalesce(Avg('humidite'), 0), humidite_max=Coalesce(Max('humidite'), 0), humidite_min=Coalesce(Min('humidite'), 0), humidite_sol_moy=Coalesce(Avg('humidite_sol'), 0), humidite_sol_max=Coalesce(Max('humidite_sol'), 0), humidite_sol_min=Coalesce(Min('humidite_sol'), 0))
			ClimatJournaliere.create(projet=noeud.projet, temperature_min=climat['temperature_min'], temperature_max=climat['temperature_max'], temperature_moy=climat['temperature_moy'], humidite_min=climat['humidite_min'], humidite_max=climat['humidite_max'], humidite_moy=climat['humidite_moy'], vent_min=climat['vent_min'], vent_max=climat['vent_max'], vent_moy=climat['vent_moy'], radiation_min=climat['radiation_min'], radiation_max=climat['radiation_max'], radiation_moy=climat['radiation_moy'], pression_min=climat['pression_min'], pression_max=climat['pression_max'], pression_moy=climat['pression_moy'], humidite_sol_moy=climat['humidite_sol_moy'], humidite_sol_max=climat['humidite_sol_max'], humidite_sol_min=climat['humidite_sol_min'], date=date_courrant)
			climats.delete()
			print('        >> Traitement est terminer avec succes.')
		else:
			print('        >>> Les donnees ont etait traiter.')
	print('    >>> NOEUDS: Terminer avec succes')
	#>>> OpenWeather
	print('    > Traitement des donnees de OpenWeather:')
	projets=Projet.objects.filter(type='O', plante__isnull=False, sol__isnull=False, polygone__isnull=False, noeud__isnull=True).distinct()
	for projet in projets:
		print('        > Traitement des donnees du projet [%s]' % projet.nom)
		climats=ClimatOpenWeather.objects.filter(projet=projet)
		if climats.exists():
			climat=climats.aggregate(temperature_moy=Coalesce(Avg('temperature'), 0), temperature_max=Coalesce(Max('temperature'), 0), temperature_min=Coalesce(Min('temperature'), 0), vent_moy=Coalesce(Avg('vent'), 0), vent_max=Coalesce(Max('vent'), 0), vent_min=Coalesce(Min('vent'), 0), radiation_moy=Coalesce(Avg('radiation'), 0), radiation_max=Coalesce(Max('radiation'), 0), radiation_min=Coalesce(Min('radiation'), 0), pression_moy=Coalesce(Avg('pression'), 0), pression_max=Coalesce(Max('pression'), 0), pression_min=Coalesce(Min('pression'), 0), humidite_moy=Coalesce(Avg('humidite'), 0), humidite_max=Coalesce(Max('humidite'), 0), humidite_min=Coalesce(Min('humidite'), 0))
			ClimatJournaliere.create(projet=projet, temperature_min=climat['temperature_min'], temperature_max=climat['temperature_max'], temperature_moy=climat['temperature_moy'], humidite_min=climat['humidite_min'], humidite_max=climat['humidite_max'], humidite_moy=climat['humidite_moy'], vent_min=climat['vent_min'], vent_max=climat['vent_max'], vent_moy=climat['vent_moy'], radiation_min=climat['radiation_min'], radiation_max=climat['radiation_max'], radiation_moy=climat['radiation_moy'], pression_max=climat['pression_max'], pression_moy=climat['pression_moy'], pression_min=climat['pression_min'], humidite_sol_max=None, humidite_sol_moy=None, humidite_sol_min=None, date=date_courrant)
			climats.delete()
			print('        >> Traitement est terminer avec succes.')
		else:
			print('        >>> Les donnees ont etait traiter.')
	print('    >>> OPENWEATHER: Terminer avec succes')
	print('    > Envoie des Message pour alerter les abonnees...')
	server=smtplib.SMTP('smtp.gmail.com', 587)
	source="pfe.2017.fst@gmail.com"
	server.ehlo()
	server.starttls()
	server.login(source, "chikibriki")
	climats=ClimatJournaliere.objects.filter(date=date_courrant)
	for climat in climats:
		#calcule de Et0
		plante=Plante({'plante': climat.projet.plante, 'date_creation_projet': climat.projet.date})
		if not plante.terminer():
			type=climat.projet.type
			if type=='O':
				objets=climat.projet.polygone.all()
			else:
				objets=Noeud.objects.filter(projet=climat.projet)
			latitude, longitude, altitude=get_latitude_moy_longitude_moy_altitude_moy(objets=objets, type=type)
			latitude=pyeto.deg2rad(latitude)
			temperature_min=climat.temperature_min
			temperature_max=climat.temperature_max
			temperature_moy=climat.temperature_moy
			vent_moy=climat.vent_moy
			radiation_moy=climat.radiation_moy
			pression_moy=climat.pression_moy
			sol_dec=pyeto.sol_dec(day_of_year)
			sha=pyeto.sunset_hour_angle(latitude, sol_dec)
			ird=pyeto.inv_rel_dist_earth_sun(day_of_year)
			et_rad=pyeto.et_rad(latitude, sol_dec, sha, ird)
			cs_rad=pyeto.cs_rad(altitude, et_rad)
			avp=pyeto.avp_from_tmin(temperature_min)
			svp=pyeto.svp_from_t(temperature_moy)
			net_rad=pyeto.net_rad(pyeto.net_in_sol_rad(radiation_moy, 0.23), pyeto.net_out_lw_rad(temperature_min, temperature_max, radiation_moy, cs_rad, avp))
			delta_svp=pyeto.delta_svp(temperature_moy)
			psy=pyeto.psy_const(pression_moy)
			Eto=pyeto.fao56_penman_monteith(net_rad, temperature_moy, vent_moy, svp, avp, delta_svp, psy, 0.0)
			#Calcule de quatite d'eau necessaire
			valeur=calculer_quantite(projet=climat.projet, Eto=Eto, humidite_sol=climat.humidite_sol_moy, sol=Sol(sol=climat.projet.sol).K, plante=plante)
			body="PROJET: %s, %s du jour: %f(l/m2)" % (climat.projet.nom, valeur['nom'], valeur['valeur'])
		else:
			body="PROJET [Etat: 'Terminer']: %s" % climat.projet.nom
		adresse_email=climat.projet.utilisateur.email
		msg=MIMEMultipart()
		msg['From']=source
		msg['To']=adresse_email
		msg['Subject']="Rapport journalier du service WATWOT"
		msg.attach(MIMEText(body, 'plain'))
		server.sendmail(source, adresse_email, msg.as_string())
		print("        > [nom: %s]: Messaged'alert est envoier." % climat.projet.nom)
	server.quit()
	print('    >>> ENVOIE: Terminer avec succes')
	print('> JOURNAL: mise a jour est terminer avec succes')

print('Remplir journal: on')
schedule.every().day.at("10:12").do(job)
while True:
	schedule.run_pending()
#	time.sleep(60)
