# coding=ISO-8859-1
from application.models import Projet as ModelProjet, Utilisateur
from application import TYPE_IRRIGATION
from datetime import date
from django import forms
import datetime

class Projet(forms.Form):
	TYPE_PROJET=(
		("O", "Superviser une surface en utilisant les fonctionnalites de openweather."),
		("N", "Superviser une surface en utilisant mes propres noeuds."),
		("P", "Superviser une plante (Presence d'un noeud au moins est obligatoire!)"),
	)
	nom=forms.CharField(label='Nom du projet', max_length=ModelProjet._meta.get_field('nom').max_length, required=False, widget=forms.TextInput(attrs={'placeholder': 'Nom'}))
	type=forms.ChoiceField(label="L'objectif de ce projet est", choices=TYPE_PROJET, widget=forms.RadioSelect(), required=False)
	type_irrigation=forms.ChoiceField(label="Type d'irrigation", required=False, choices=TYPE_IRRIGATION)

	def __init__(self, *args, **kwargs):
		self.nom=kwargs.pop('nom', None)
		self.type_irrigation=kwargs.pop('type_irrigation', None)
		self.type=kwargs.pop('type', None)
		super(Projet, self).__init__(*args, **kwargs)

	def is_valid(self):
		nom=self.data['nom']
		if not nom:
			self.add_error("nom", "Champ Nom vide!")
		type_irrigation=self.data['type_irrigation']
		if not type_irrigation:
			self.add_error("type_irrigation", "Selectionner une option!")
		type=self.data.get('type', None)
		if not type:
			self.add_error("type", "Choisir un choix!")
		return super(Projet, self).is_valid()

	def enregistrer(self, pseudo):
		nom=self.cleaned_data['nom']
		type_irrigation=self.cleaned_data['type_irrigation']
		type=self.cleaned_data['type']
		projet=ModelProjet.create(nom=nom, type_irrigation=type_irrigation, pseudo=pseudo, type=type)
		return projet
