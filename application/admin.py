from django.contrib import admin
from application.models import Utilisateur, Polygone, Projet,  Plante, Noeud, Sol, ClimatJournaliere


class UtilisateurAdmin(admin.ModelAdmin):
	list_display=['id', 'nom', 'prenom', 'pseudo', 'mot_de_passe', 'adresse', 'position', 'telephone', 'email']
	search_fields=list_display
admin.site.register(Utilisateur, UtilisateurAdmin)


class PolygoneAdmin(admin.ModelAdmin):
	list_display=['id', 'polygone']
	search_fields=list_display
admin.site.register(Polygone, PolygoneAdmin)


class SolAdmin(admin.ModelAdmin):
	list_display=['id', 'nom', 'sable', 'argile', 'limon', 'utilisateur']
	search_fields=['id', 'nom', 'sable', 'argile', 'limon', 'utilisateur']
admin.site.register(Sol, SolAdmin)


class ProjetAdmin(admin.ModelAdmin):
	list_display=['id', 'nom', 'date', 'utilisateur', 'type_irrigation', 'sol', 'plante', 'type']
	search_fields=['id', 'nom', 'date', 'type_irrigation', 'type']
admin.site.register(Projet, ProjetAdmin)


class PlanteAdmin(admin.ModelAdmin):
	list_display=['id', 'nom', 'initial', 'initial_Kc', 'developpement', 'developpement_Kc', 'mi_saison', 'mi_saison_Kc', 'recolte', 'recolte_Kc', 'par']
	search_fields=list_display
admin.site.register(Plante, PlanteAdmin)


class NoeudAdmin(admin.ModelAdmin):
	list_display=['identifiant_arduino', 'projet', 'altitude', 'position', 'temperature', 'humidite', 'vent', 'radiation', 'humidite_sol']
	search_fields=['identifiant_arduino', 'altitude', 'position', 'temperature', 'humidite', 'vent', 'radiation', 'humidite_sol']
admin.site.register(Noeud, NoeudAdmin)


class ClimatJournaliereAdmin(admin.ModelAdmin):
	list_display=['id', 'temperature_min', 'temperature_max', 'temperature_moy', 'humidite_min', 'humidite_max', 'humidite_moy', 'vent_min', 'vent_max', 'vent_moy', 'radiation_min', 'radiation_max', 'radiation_moy', 'pression_min', 'pression_max', 'pression_moy', 'date']
	search_fields=list_display
admin.site.register(ClimatJournaliere, ClimatJournaliereAdmin)
