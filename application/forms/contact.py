# coding=ISO-8859-1
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from email.MIMEMultipart import MIMEMultipart
from smtplib import SMTPAuthenticationError
from application.models import Utilisateur
from email.MIMEText import MIMEText
from django import forms
import smtplib

class Email(forms.Form):
	nom=forms.CharField(label='', max_length=Utilisateur._meta.get_field('nom').max_length, required=False, widget=forms.TextInput(attrs={'placeholder': 'Nom', 'id': 'message', 'class': 'form-control'}))
	email=forms.CharField(label='', max_length=Utilisateur._meta.get_field('email').max_length, required=False, widget=forms.TextInput(attrs={'placeholder': 'Votre email', 'id': 'message', 'class': 'form-control'}))
	message=forms.CharField(label='', max_length=300, required=False, widget=forms.Textarea(attrs={'placeholder': 'Message', 'id': 'message', 'class': 'form-control'}))

	def __init__(self, *args, **kwargs):
		self.nom=kwargs.pop('nom', None)
		self.email=kwargs.pop('email', None)
		self.message=kwargs.pop('message', None)
		super(Email, self).__init__(*args, **kwargs)

	def is_valid(self):
		nom=self.data['nom']
		if not nom:
			self.add_error("nom", "Saisir votre nom!")
		email=self.data['email']
		if not email:
			self.add_error("email", "Saisir votre email!")
		message=self.data['message']
		if not message:
			self.add_error("message", "Message est vide!")
		return super(Email, self).is_valid()

	def envoyer_message(self):
		nom=self.cleaned_data['nom']
		email=self.cleaned_data['email']
		message=self.cleaned_data['message']
		msg=MIMEMultipart()
		msg['To']="pfe.2017.fst@gmail.com"
		msg['From']=email
		msg['Subject']="Consultation: %s a un problem" % nom
		msg.attach(MIMEText(message, 'plain'))
		server=smtplib.SMTP('smtp.gmail.com', 587)
		server.ehlo()
		server.starttls()
		server.login(msg['To'], "chikibriki")
		server.sendmail(msg['To'], msg['To'], msg.as_string())
		server.quit()
