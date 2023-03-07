# coding=ISO-8859-1
from email.MIMEMultipart import MIMEMultipart
from application.models import Utilisateur
from application import mot_de_passe_hash
from email.MIMEText import MIMEText
from email.MIMEText import MIMEText
from django import forms
import smtplib

class Mdp(forms.Form):
	mot_de_passe=forms.CharField(label='Ancien mot de passe', max_length=Utilisateur._meta.get_field('mot_de_passe').max_length, required=False, widget=forms.PasswordInput(attrs={'placeholder': 'Ancien'}))
	nouveau=forms.CharField(label='Nouveau mot de passe', max_length=Utilisateur._meta.get_field('mot_de_passe').max_length, required=False, widget=forms.PasswordInput(attrs={'placeholder': 'Nouveau'}))
	confirmation=forms.CharField(label='Resaissir le nouveau mot de passe', max_length=Utilisateur._meta.get_field('mot_de_passe').max_length, required=False, widget=forms.PasswordInput(attrs={'placeholder': 'Confirmation'}))

	def __init__(self, *arg, **kwarg):
		self.mot_de_passe=kwarg.pop('mot_de_passe', None)
		self.nouveau=kwarg.pop('nouveau', None)
		self.confirmation=kwarg.pop('confirmation', None)
		super(Mdp, self).__init__(*arg, **kwarg)

	def is_valid(self, pseudo):
		mot_de_passe=self.data['mot_de_passe']
		nouveau=self.data['nouveau']
		confirmation=self.data['confirmation']
		if not mot_de_passe:
			self.add_error("mot_de_passe", "Saissir votre mot de passe")
		elif not Utilisateur.objects.filter(pseudo=pseudo, mot_de_passe=mot_de_passe).exists():
			self.add_error("mot_de_passe", "Mot de passe est Incorrect")
		else:
			if not nouveau:
				self.add_error("nouveau", "Saisiir le nouveau mot de passe")
			else:
				if not confirmation:
					self.add_error("confirmation", "Saisiir le nouveau mot de passe pour confirmer")
				else:
					if confirmation!=nouveau:
						self.add_error("confirmation", "Mot de passe est incorrect!")
		valeur=super(Mdp, self).is_valid()
		if not valeur and mot_de_passe:
			self.add_error("mot_de_passe", "Resaissir votre mot de passe")
			if not valeur and nouveau:
				self.add_error("nouveau", "Resaissir le nouveau mot de passe")
				if not valeur and confirmation:
					self.add_error("confirmation", "Resaissir le nouveau mot de passe de confirmation")
		return valeur

	def enregistrer(self, pseudo):
		nouveau=self.cleaned_data['nouveau']
		email=Utilisateur.objects.get(pseudo=pseudo).email
		msg=MIMEMultipart()
		msg['From']="pfe.2017.fst@gmail.com"
		msg['To']=email
		msg['Subject']="Nouveau mot de passe"
		msg.attach(MIMEText(nouveau, 'plain'))
		#error
		server=smtplib.SMTP('smtp.gmail.com', 587)
		server.ehlo()
		server.starttls()
		server.login(msg['From'], "chikibriki")
		server.sendmail(msg['To'], msg['From'], msg.as_string())
		server.quit()
		Utilisateur.update(pseudo=pseudo, mot_de_passe=nouveau)
		return mot_de_passe_hash(nouveau)
