from application.models import ClimatNoeud
from rest_framework import serializers

class ClimatSerializer(serializers.ModelSerializer):
	class Meta:
		model=ClimatNoeud
		fields=('noeud', 'temperature', 'humidite', 'vent', 'radiation', 'pression', 'humidite_sol')
