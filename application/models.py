from application import to_float, mot_de_passe_hash, TYPE_IRRIGATION, TYPE_PROJET
from application import set_utilisateur_nom, get_altitude
from django.contrib.gis.geos import GEOSGeometry, Point
from django.contrib.gis.db import models as gisModels
from django.db.models import Q
from django.db import models
from ast import literal_eval
import uuid
import os


class Polygone(gisModels.Model):
	polygone=gisModels.GeometryField(srid=4326)

	@classmethod
	def create(cls, geos_geometry):
		geometry=GEOSGeometry(geos_geometry.__str__())
		polygone=cls.objects.filter(polygone=geometry).first()
		if not polygone:
			polygone=cls(polygone=geometry)
			polygone.save()
		return polygone

	def __str__(self):
		return self.polygone.__str__()

	class Meta:
		managed=True
		db_table='polygone'


class Plante(models.Model):
	nom=models.CharField(max_length=20)
	CHOIX=(('J', 'Jour'), ('S', 'Semaine'), ('M', 'Mois'))
	initial=models.IntegerField()
	initial_Kc=models.FloatField()
	developpement=models.IntegerField()
	developpement_Kc=models.FloatField()
	mi_saison=models.IntegerField()
	mi_saison_Kc=models.FloatField()
	recolte=models.IntegerField()
	recolte_Kc=models.FloatField()
	par=models.CharField(max_length=1, choices=CHOIX)

	def __str__(self):
		return self.nom

	class Meta:
		managed=True
		db_table='plante'


class Utilisateur(gisModels.Model):
	nom=gisModels.CharField(max_length=20)
	prenom=gisModels.CharField(max_length=20)
	pseudo=gisModels.CharField(max_length=20, unique=True)
	mot_de_passe=gisModels.CharField(max_length=33)
	photo=gisModels.ImageField(upload_to=set_utilisateur_nom)
	telephone=gisModels.IntegerField()
	email=gisModels.CharField(max_length=40)
	adresse=gisModels.CharField(max_length=50)
	position=gisModels.PointField()
	plante=gisModels.ManyToManyField(Plante)

	@classmethod
	def create(cls, nom, prenom, pseudo, mot_de_passe, telephone, longitude, latitude, adresse, email, photo):
		position=Point(to_float(longitude), to_float(latitude))
		utilisateur=cls(nom=nom, prenom=prenom, pseudo=pseudo, mot_de_passe=mot_de_passe, telephone=telephone, email=email, position=position, adresse=adresse, photo=photo)
		utilisateur.save()
		return utilisateur

	@classmethod
	def supprimer_photo(cls, pseudo):
		utilisateur=cls.objects.get(pseudo=pseudo)
		utilisateur.photo=None
		utilisateur.save()
		return utilisateur

	@classmethod
	def update(cls, pseudo, nom=None, prenom=None, mot_de_passe=None, telephone=None, longitude=None, latitude=None, adresse=None, email=None, photo=None):
		utilisateur=cls.objects.get(pseudo=pseudo)
		if mot_de_passe:
			utilisateur.mot_de_passe=mot_de_passe
		if photo:
			utilisateur.photo=photo
		if nom:
			utilisateur.nom=nom
		if prenom:
			utilisateur.prenom=prenom
		if telephone:
			utilisateur.telephone=telephone
		if adresse:
			utilisateur.adresse=adresse
		if latitude and longitude:
			utilisateur.position=Point(to_float(longitude), to_float(latitude))
		if email:
			utilisateur.email=email
		utilisateur.save()
		return utilisateur

	@classmethod
	def exists(cls, pseudo, mot_de_passe):
		utilisateur=cls.objects.filter(pseudo=pseudo).first()
		if utilisateur:
			if mot_de_passe==mot_de_passe_hash(utilisateur.mot_de_passe):
				return utilisateur
		return None

	def __str__(self):
		return 'Utilisateur: %s %s, Pseudo: %s' % (self.nom, self.prenom, self.pseudo)

	class Meta:
		managed=True
		db_table='utilisateur'


class Sol(models.Model):
	nom=models.CharField(max_length=20)
	sable=models.FloatField()
	argile=models.FloatField()
	limon=models.FloatField()
	utilisateur=models.ForeignKey(Utilisateur)

	def __str__(self):
		return self.nom

	class Meta:
		managed=True
		db_table='sol'


class Projet(models.Model):
	nom=models.CharField(max_length=50)
	date=models.DateTimeField(auto_now_add=True)
	utilisateur=models.ForeignKey(Utilisateur)
	type_irrigation=models.CharField(max_length=1, choices=TYPE_IRRIGATION)
	sol=models.ForeignKey(Sol, null=True, blank=True)
	plante=models.ForeignKey(Plante, null=True, blank=True)
	polygone=models.ManyToManyField(Polygone)
	type=models.CharField(max_length=1, choices=TYPE_PROJET)

	@classmethod
	def create(cls, nom, pseudo, type_irrigation, type):
		utilisateur=Utilisateur.objects.get(pseudo=pseudo)
		projet=cls(nom=nom, utilisateur=utilisateur, type_irrigation=type_irrigation, type=type)
		projet.save()
		return projet

	@classmethod
	def supprimer(cls, id):
		not_projet_all_polygones=list(cls.objects.filter(~Q(id=id)).distinct().values_list('polygone', flat=True))
		projet=cls.objects.get(id=id)
		polygones=projet.polygone.all()
		noeuds=Noeud.objects.filter(projet=projet)
		climats_noeuds=ClimatNoeud.objects.filter(noeud=noeuds)
		climats_open_weather=ClimatOpenWeather.objects.filter(projet=projet)
		climats_journalieres=ClimatJournaliere.objects.filter(projet=projet)
		for polygone in polygones:
			if not polygone.id in not_projet_all_polygones:
				polygone.delete()
		noeuds.delete()
		climats_noeuds.delete()
		climats_open_weather.delete()
		climats_journalieres.delete()
		projet.delete()

	@classmethod
	def add_polygones(cls, projet_id, geojson):
		projet=cls.objects.get(id=projet_id)
		features=geojson['features']
		for feature in features:
			geos_geometry=feature['geometry']
			polygone=Polygone.create(geos_geometry=geos_geometry)
			projet.polygone.add(polygone)

	def __str__(self):
		if (self.type!='P' and not self.polygone.exists()) or not self.plante or not self.sol or (self.type!='O' and not Noeud.objects.filter(projet=self.id).exists()):
			return 'PROJET INCOMPLET: %s' % self.nom
		return '[Date de Creation: %s]         %s' % (self.date.date().__str__(), self.nom)

	class Meta:
		managed=True
		db_table='projet'


class Noeud(gisModels.Model):
	identifiant_arduino=gisModels.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
	projet=models.ForeignKey(Projet)
	position=gisModels.PointField()
	altitude=gisModels.FloatField()
	temperature=gisModels.BooleanField()
	humidite=gisModels.BooleanField()
	vent=gisModels.BooleanField()
	radiation=gisModels.BooleanField()
	humidite_sol=gisModels.BooleanField()

	@classmethod
	def create(cls, geojson, projet):
		features=geojson['features']
		projet=Projet.objects.get(id=projet)
		for feature in features:
			geos_geometry=feature['geometry']
			latitude=geos_geometry['coordinates'][0][0][0]
			longitude=geos_geometry['coordinates'][0][0][1]
			altitude=get_altitude(latitude=latitude, longitude=longitude)
			if altitude:
				position=Point(to_float(longitude), to_float(latitude))
				properties=feature['properties']
				temperature=properties['temperature et humidite']
				humidite=temperature
				vent=properties['vent']
				radiation=properties['radiation solaire']
				humidite_sol=properties['humidite de sol']
				noeud=cls(projet=projet, position=position, temperature=temperature, humidite=humidite, vent=vent, radiation=radiation, humidite_sol=humidite_sol, altitude=altitude)
				noeud.save()

	def __str__(self):
		return self.identifiant_arduino.__str__()

	class Meta:
		managed=True
		db_table='noeud'


class Climat(models.Model):
	temperature=models.FloatField()
	humidite=models.FloatField()
	vent=models.FloatField()
	radiation=models.FloatField()
	pression=models.FloatField()
	humidite_sol=models.FloatField(null=True, blank=True, default=None)
	date=models.DateField(auto_now_add=True)
	time=models.TimeField(auto_now_add=True)

	class Meta:
		managed=True
		db_table='climat'


class ClimatNoeud(Climat):
	noeud=models.ForeignKey(Noeud)

	class Meta:
		managed=True
		db_table='climat_noeud'


class ClimatOpenWeather(Climat):
	projet=models.ForeignKey(Projet)

	class Meta:
		managed=True
		db_table='climat_openWeather'


class ClimatJournaliere(models.Model):
	projet=models.ForeignKey(Projet)
	temperature_min=models.FloatField()
	temperature_moy=models.FloatField()
	temperature_max=models.FloatField()
	humidite_min=models.FloatField()
	humidite_moy=models.FloatField()
	humidite_max=models.FloatField()
	humidite_sol_min=models.FloatField(null=True, blank=True)
	humidite_sol_moy=models.FloatField(null=True, blank=True)
	humidite_sol_max=models.FloatField(null=True, blank=True)
	vent_min=models.FloatField()
	vent_moy=models.FloatField()
	vent_max=models.FloatField()
	radiation_min=models.FloatField()
	radiation_moy=models.FloatField()
	radiation_max=models.FloatField()
	pression_min=models.FloatField()
	pression_moy=models.FloatField()
	pression_max=models.FloatField()
	date=models.DateField()

	@classmethod
	def create(cls, projet, temperature_min, temperature_moy, temperature_max, humidite_min, humidite_moy, humidite_max, vent_min, vent_moy, vent_max, radiation_min, radiation_moy, radiation_max, pression_min, pression_moy, pression_max, humidite_sol_min, humidite_sol_moy,  humidite_sol_max, date):
		journal=cls(projet=projet, temperature_min=temperature_min, temperature_moy=temperature_moy, temperature_max=temperature_max, humidite_min=humidite_min, humidite_moy=humidite_moy, humidite_max=humidite_max, humidite_sol_min=humidite_sol_min, humidite_sol_moy=humidite_sol_moy, humidite_sol_max=humidite_sol_max, vent_min=vent_min, vent_moy=vent_moy, vent_max=vent_max, radiation_min=radiation_min, radiation_moy=radiation_moy, radiation_max=radiation_max, pression_min=pression_min, pression_moy=pression_moy, pression_max=pression_max, date=date)
		journal.save()

	class Meta:
		managed=True
		db_table='journal'

"""
class Verification(models.Model):
	utilisateur=models.ForeignKey(Utilisateur)
	cle=models.UUIDField(default=uuid.uuid4)

	@classmethod
	def create(cls, utilisateur):
		utilisateur.objects.get(id=utilisateur)
		verification=cls(utilisateur=utilisateur)
		verification.save()

	@classmethod
	def supprimer(cls, utilisateur, cle):
		verification=cls.objects.filter(id=utilisateur, cle=cle)
		if verification.exists():
			verification.first().delete()
			return True
		return False

	class Meta:
		managed=True
		db_table='verification'
"""
