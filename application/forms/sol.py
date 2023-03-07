# coding=ISO-8859-1
from django import forms
from application.models import Sol as ModelSol, Projet, Utilisateur

class Sol(forms.Form):
	nom=forms.CharField(label='Nom de votre terrain:', max_length=ModelSol._meta.get_field('nom').max_length, required=False, widget=forms.TextInput(attrs={'placeholder': 'Nom du terrain'}))
	sable=forms.FloatField(required=False, widget=forms.NumberInput(attrs={'min': '0'}))
	argile=forms.FloatField(required=False, widget=forms.NumberInput(attrs={'min': '0'}))
	limon=forms.FloatField(required=False, widget=forms.NumberInput(attrs={'min': '0'}))

	def __init__(self, *args, **kwargs):
		self.nom=kwargs.pop('nom', None)
		self.sable=kwargs.pop('sable', None)
 		self.argile=kwargs.pop('argile', None)
 		self.limon=kwargs.pop('limon', None)
		super(Sol, self).__init__(*args, **kwargs)

	def is_valid(self):
                somme=0.0
		nom=self.data['nom']
		if not nom:
			self.add_error("nom", "Ajouter un nom!")
		sable=self.data['sable']
		if not sable:
			self.add_error("sable", "Saisir une valeur non null!")
		else:
                        sable=float(sable)
                        somme=somme+sable
                        if sable==0:
                                self.add_error("sable", "Saisir une valeur!")
                        elif sable<0:
                                self.add_error("sable", "Saisir une valeur positive!")
		argile=self.data['argile']
		if not argile:
			self.add_error("argile", "Saisir une valeur non null!")
		else:
                        argile=float(argile)
                        somme=somme+argile
                        if argile==0:
                                self.add_error("argile", "Saisir une valeur!")
                        elif argile<0:
                        	self.add_error("argile", "Saisir une valeur positive!")
		limon=self.data['limon']
		if not limon:
			self.add_error("limon", "Saisir une valeur non null!")
                else:
                        limon=float(limon)
                        somme=somme+limon
                        if limon==0:
                                self.add_error("limon", "Saisir une valeur!")
                        elif limon<0:
                                self.add_error("limon", "Saisir une valeur positive!")
                if somme!=0.0 and somme!=100.0 and somme!=100.1 and somme!=99.9:
			self.add_error("sable", "Les valeurs sont incorrects!")
		return super(Sol, self).is_valid()

	def enregistrer(self, projet, pseudo):
		nom=self.cleaned_data['nom']
		sable=float(self.cleaned_data['sable'])
		argile=float(self.cleaned_data['argile'])
		limon=float(self.cleaned_data['limon'])
		projet=Projet.objects.get(id=projet)
		utilisateur=Utilisateur.objects.get(pseudo=pseudo)
		somme=sable+argile+limon
		if somme==100.1:
                        sable=sable-0.1
                elif somme==99.9:
                        sable=sable+0.1
		sol=ModelSol(nom=nom, sable=sable, argile=argile, limon=limon, utilisateur=utilisateur)
		sol.save()
		projet.sol=sol
		projet.save()

class ChoixSol(forms.Form):
	sol=forms.IntegerField(required=False, widget=forms.HiddenInput())

	def __init__(self, *args, **kwargs):
		self.sol=kwargs.pop('sol', None)
		super(ChoixSol, self).__init__(*args, **kwargs)

	def is_valid(self):
		sol=self.data['sol']
		if not sol:
			self.add_error("", "Selectionner un sol!")
		elif not ModelSol.objects.filter(id=sol).exists():
			self.add_error("", "Sol Incorrect!")
		return super(ChoixSol, self).is_valid()

	def enregistrer(self, projet, pseudo):
		sol=self.cleaned_data['sol']
		sol=ModelSol.objects.get(utilisateur__pseudo=pseudo, id=sol)
		projet=Projet.objects.get(id=projet)
		projet.sol=sol
		projet.save()
