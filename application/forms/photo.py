# coding=ISO-8859-1
from application.models import Utilisateur
from django import forms

class Photo(forms.Form):
	photo=forms.ImageField(label='Photo', required=False, widget=forms.FileInput(attrs={'placeholder': 'Selectionner une image'}))

	def __init__(self, *arg, **kwarg):
		photo=kwarg.pop('photo', None)
		super(Photo, self).__init__(*arg, **kwarg)

	def is_valid(self):
		photo=self.data['photo']
		if not photo:
			self.add_error("photo", "Selectionner un photo")
		return super(Photo, self).is_valid()

	def enregistrer(self, pseudo):
		photo=self.data['photo']
		Utilisateur.update(pseudo=pseudo, photo=photo)
