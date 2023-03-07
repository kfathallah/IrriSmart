# coding=ISO-8859-1
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from application.models import Utilisateur
from application import mot_de_passe_hash
from django import forms

class Inscription(forms.Form):
	nom=forms.CharField(label='Nom', max_length=Utilisateur._meta.get_field('nom').max_length, required=False, widget=forms.TextInput(attrs={'placeholder': 'Nom'}))
	prenom=forms.CharField(label='Prenom', max_length=Utilisateur._meta.get_field('prenom').max_length, required=False, widget=forms.TextInput(attrs={'placeholder': 'Prenom'}))
	pseudo=forms.CharField(label='Pseudo', max_length=Utilisateur._meta.get_field('pseudo').max_length, required=False, widget=forms.TextInput(attrs={'placeholder': 'Pseudo'}))
	mot_de_passe=forms.CharField(label='Mot de passe', max_length=Utilisateur._meta.get_field('mot_de_passe').max_length, required=False, widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}))
	confirmation_mot_de_passe=forms.CharField(label='Confirmer le mot de passe', max_length=Utilisateur._meta.get_field('mot_de_passe').max_length, required=False, widget=forms.PasswordInput(attrs={'placeholder': 'Resaissir le mot de passe'}))
	adresse=forms.CharField(label='adresse', max_length=Utilisateur._meta.get_field('adresse').max_length, required=False, widget=forms.TextInput(attrs={'id': 'searchTextField', 'placeholder': 'Saisir une adresse', 'class': 'form-control', 'autocomplete': 'on', 'runat': 'server'}))
	photo=forms.FileField(label='Photo', required=False, widget=forms.FileInput(attrs={'placeholder': 'Selectionner une image'}))
	email=forms.CharField(label='Email', max_length=Utilisateur._meta.get_field('email').max_length, required=False, widget=forms.TextInput(attrs={'placeholder': 'E-Mail'}))
	telephone=forms.CharField(label='Telephone', required=False, widget=forms.TextInput(attrs={'placeholder': 'Téléphone'}))
	latitude=forms.FloatField(required=False, widget=forms.HiddenInput(attrs={'id': 'cityLat', 'name': 'cityLat'}))
	longitude=forms.FloatField(required=False, widget=forms.HiddenInput(attrs={'id': 'cityLng', 'name': 'cityLng'}))

	def __init__(self, *args, **kwargs):
		self.nom=kwargs.pop('nom', None)
		self.prenom=kwargs.pop('prenom', None)
		self.pseudo=kwargs.pop('pseudo', None)
		self.mot_de_passe=kwargs.pop('mot_de_passe', None)
		self.mot_de_passe=kwargs.pop('confirmation_mot_de_passe', None)
		self.email=kwargs.pop('email', None)
		self.telephone=kwargs.pop('telephone', None)
		self.adresse=kwargs.pop('adresse', None)
		self.latitude=kwargs.pop('latitude', None)
		self.longitude=kwargs.pop('longitude', None)
		self.photo=kwargs.pop('photo', None)
		super(Inscription, self).__init__(*args, **kwargs)

	def is_valid(self):
		nom=self.data['nom']
		if not nom:
			self.add_error("nom", "Nom est vide!")
		elif any(char.isdigit() for char in nom):
			self.add_error("nom", "Nom est incorrect!")
		prenom=self.data['prenom']
		if not prenom:
			self.add_error("prenom", "Prenom est vide!")
		elif any(char.isdigit() for char in prenom):
			self.add_error("prenom", "Prenom est incorrect!")
		pseudo=self.data['pseudo']
		if not pseudo:
			self.add_error("pseudo", "Pseudo est vide!")
		elif Utilisateur.objects.filter(pseudo=pseudo).exists():
			self.add_error("pseudo", "Pseudo déja existant!")
		email=self.data['email']
		if not email:
			self.add_error("email", "Email est vide!")
		else:
			try:
				validate_email(email)
			except ValidationError:
				self.add_error("email", "Email est Incorrect!")
		telephone=self.data['telephone']
		if not telephone:
			self.add_error("telephone", "Téléphone est vide!")
		elif not telephone.isdigit():
			self.add_error("telephone", "Téléphone est incorrect!")
		adresse=self.data['adresse']
		if not adresse:
			self.add_error("adresse", "Address est vide!")
		else:
			latitude=self.data['latitude']
			longitude=self.data['longitude']
			if not latitude or not longitude:
				self.add_error("adresse", "Address est Invalide!")
		confirmation_mot_de_passe=self.data['confirmation_mot_de_passe']
		if not confirmation_mot_de_passe:
			self.add_error("confirmation_mot_de_passe", "Resaissir le mot de passe!")
		mot_de_passe=self.data['mot_de_passe']
		if not mot_de_passe:
			self.add_error("mot_de_passe", "Mot de pass est vide!")
		else:
			if confirmation_mot_de_passe:
				if confirmation_mot_de_passe!=mot_de_passe:
					self.add_error("mot_de_passe", "Mot de passe est Incorrect!")
		value=super(Inscription, self).is_valid()
		if not value and mot_de_passe:
			self.add_error("mot_de_passe", "Ressaisir le Mot de pass.")
		return value

	def enregistrer(self):
		nom=self.cleaned_data['nom']
		prenom=self.cleaned_data['prenom']
		pseudo=self.cleaned_data['pseudo']
		mot_de_passe=self.cleaned_data['mot_de_passe']
		email=self.cleaned_data['email']
		telephone=self.cleaned_data['telephone']
		adresse=self.cleaned_data['adresse']
		latitude=self.cleaned_data['latitude']
		longitude=self.cleaned_data['longitude']
		photo=self.cleaned_data['photo']
		Utilisateur.create(nom=nom, prenom=prenom, pseudo=pseudo, mot_de_passe=mot_de_passe, email=email, telephone=telephone, latitude=latitude, longitude=longitude, adresse=adresse, photo=photo)

	def get(self, valeur):
		if valeur=='mot_de_passe':
			return mot_de_passe_hash(self.data['mot_de_passe'])
		return self.data[valeur]
