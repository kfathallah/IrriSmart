# coding=ISO-8859-1
from application.models import Projet, Plante as ModelPlante, Utilisateur
from django import forms

class Plante(forms.Form):
	nom=forms.CharField(label='Nom de votre plante', max_length=ModelPlante._meta.get_field('nom').max_length, required=False, widget=forms.TextInput(attrs={'placeholder': 'Nom du plante'}))
	par=forms.ChoiceField(label='Par', required=False, choices=ModelPlante.CHOIX)
	initial=forms.IntegerField(label='', required=False,min_value=0,max_value=366, widget=forms.NumberInput(attrs={}))
	initial_Kc=forms.FloatField(label='', required=False,max_value=1.4, min_value=0, widget=forms.NumberInput(attrs={'step': "0.01"}))
	developpement=forms.IntegerField(label='', required=False, min_value=0,max_value=366,widget=forms.NumberInput(attrs={}))
	developpement_Kc=forms.FloatField(label='', required=False,max_value=1.4, min_value=0, widget=forms.NumberInput(attrs={'step': "0.01"}))
	mi_saison=forms.IntegerField(label='', required=False, min_value=0,max_value=366,widget=forms.NumberInput(attrs={}))
	mi_saison_Kc=forms.FloatField(label='', required=False, max_value=1.4, min_value=0,widget=forms.NumberInput(attrs={'step': "0.01"}))
	recolte=forms.IntegerField(label='', required=False, min_value=0, max_value=366,widget=forms.NumberInput(attrs={}))
	recolte_Kc=forms.FloatField(label='', required=False,max_value=1.4, min_value=0, widget=forms.NumberInput(attrs={'step': "0.01"}))

	def __init__(self, *args, **kwargs):
		self.nom=kwargs.pop('nom', None)
		self.initial=kwargs.pop('initial', None)
		self.initial_Kc=kwargs.pop('initial_Kc', None)
		self.developpement=kwargs.pop('developpement', None)
		self.developpement_Kc=kwargs.pop('developpement_Kc', None)
		self.mi_saison=kwargs.pop('mi_saison', None)
		self.mi_saison_Kc=kwargs.pop('mi_saison_Kc', None)
		self.recolte=kwargs.pop('recolte', None)
		self.recolte_Kc=kwargs.pop('recolte_Kc', None)
		self.par=kwargs.pop('par', None)
		super(Plante, self).__init__(*args, **kwargs)

	def is_valid(self):
		nom=self.data['nom']
		if not nom:
			self.add_error("nom", "Nom du plante: Ajouter un nom!")
		initial=self.data['initial']
		if not initial:
			self.add_error("", "initial: Ajouter une valeur!")
		initial_Kc=self.data['initial_Kc']
		if not initial_Kc:
			self.add_error("", "initial Kc: Ajouter une valeur!")
		developpement=self.data['developpement']
		if not developpement:
			self.add_error("", "developpement: Ajouter une valeur!")
		developpement_Kc=self.data['developpement_Kc']
		if not developpement_Kc:
			self.add_error("", "developpement Kc: Ajouter une valeur!")
		mi_saison=self.data['mi_saison']
		if not mi_saison:
			self.add_error("", "mi-saison: Ajouter une valeur!")
		mi_saison_Kc=self.data['mi_saison_Kc']
		if not mi_saison_Kc:
			self.add_error("", "mi-saison Kc: Ajouter une valeur!")
		recolte=self.data['recolte']
		if not recolte:
			self.add_error("", "recolte: Ajouter une valeur!")
		recolte_Kc=self.data['recolte_Kc']
		if not recolte_Kc:
			self.add_error("", "recolte Kc: Ajouter une valeur!")
		return super(Plante, self).is_valid()

	def enregistrer(self, projet, pseudo):
		nom=self.cleaned_data['nom']
		initial=self.cleaned_data['initial']
		initial_Kc=self.cleaned_data['initial_Kc']
		developpement=self.cleaned_data['developpement']
		developpement_Kc=self.cleaned_data['developpement_Kc']
		mi_saison=self.cleaned_data['mi_saison']
		mi_saison_Kc=self.cleaned_data['mi_saison_Kc']
		recolte=self.cleaned_data['recolte']
		recolte_Kc=self.cleaned_data['recolte_Kc']
		par=self.cleaned_data['par']
		plante=ModelPlante(nom=nom, initial=initial, initial_Kc=initial_Kc, developpement=developpement, developpement_Kc=developpement_Kc, mi_saison=mi_saison, mi_saison_Kc=mi_saison_Kc, recolte=recolte, recolte_Kc=recolte_Kc, par=par)
		plante.save()
		utilisateur=Utilisateur.objects.get(pseudo=pseudo)
		utilisateur.plante.add(plante)
		projet=Projet.objects.get(id=projet)
		projet.plante=plante
		projet.save()

class ChoixPlante(forms.Form):
	plante=forms.IntegerField(required=False, widget=forms.HiddenInput())

	def __init__(self, *args, **kwargs):
		self.plante=kwargs.pop('plante', None)
		super(ChoixPlante, self).__init__(*args, **kwargs)

	def is_valid(self):
		plante=self.data['plante']
		if not plante:
			self.add_error("", "Selectionner une plante!")
		elif not ModelPlante.objects.filter(id=plante).exists():
			self.add_error("", "Plante Incorrect!")
		return super(ChoixPlante, self).is_valid()

	def enregistrer(self, projet, pseudo):
		plante=ModelPlante.objects.get(id=self.cleaned_data['plante'])
		projet=Projet.objects.get(id=projet)
		projet.plante=plante
		projet.save()
