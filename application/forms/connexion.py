# coding=ISO-8859-1
from application.models import Utilisateur
from application import mot_de_passe_hash
from django import forms

class Connexion(forms.Form):
	pseudo=forms.CharField(label='Pseudo', max_length=Utilisateur._meta.get_field('pseudo').max_length, required=False, widget=forms.TextInput(attrs={'placeholder': 'Pseudo'}))
	mot_de_passe=forms.CharField(label='Mot de passe', max_length=Utilisateur._meta.get_field('mot_de_passe').max_length, required=False, widget=forms.PasswordInput(attrs={'placeholder': 'Mot de pass'}))

	def __init__(self, *args, **kwargs):
		self.pseudo=kwargs.pop('pseudo', None)
		self.mot_de_passe=kwargs.pop('mot_de_passe', None)
		super(Connexion, self).__init__(*args, **kwargs)

	def is_valid(self):
		mot_de_passe=self.data['mot_de_passe']
		if not mot_de_passe:
			self.add_error("mot_de_passe", "Mot de pass est vide!")
		pseudo=self.data['pseudo']
		if not pseudo:
			self.add_error("pseudo", "Pseudo est vide!")
		else:
			if mot_de_passe:
				mot_de_passe=mot_de_passe_hash(mot_de_passe)
				if not Utilisateur.exists(pseudo=pseudo, mot_de_passe=mot_de_passe):
					self.add_error("", "Pseudo/Mot de passe est Incorrect!")
		return super(Connexion, self).is_valid()

	def get(self, valeur):
		if valeur=='mot_de_passe':
			return mot_de_passe_hash(self.data['mot_de_passe'])
		return self.data[valeur]
