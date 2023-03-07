from .views.profile import index as formulaire_profile, valider as valider_profile, supprimer_photo, photo, valider_photo, valider_mot_de_passe, mot_de_passe
from .views.projet import index as mes_projets, projet, creation_projet, valider_projet, update_donnees, supprimer_projet
from .views.acceuil import index as acceuil, connexion, valider as valider_connexion, deconnexion, envoyer_message
from .views.inscription import index as formulaire_inscription, valider as valider_inscription
from .views.parcelle import index as creation_parcelle, importer_polygone, valider_parcelle
from .views.plante import choix_plante, valider_choix_plante, plante, valider_plante
from .views.climat_noeud import sauvegarder_donnees_noeud as data_noeud
from .views.sol import choix_sol, valider_choix_sol, sol, valider_sol
from .views.noeud import index as noeud, valider_noeud
from django.conf.urls import url

urlpatterns=[
    url(r'^$', acceuil, name='acceuil'),
    url(r'^envoyer-message/$', envoyer_message, name='envoyer_message'),
    url(r'^connexion/$', connexion, name='connexion'),
    url(r'^connexion/validation/$', valider_connexion, name='valider_connexion'),
    url(r'^deconnexion/$', deconnexion, name='deconnexion'),
    url(r'^inscription/$', formulaire_inscription, name='inscription'),
    url(r'^inscription/validation/$', valider_inscription, name='valider_inscription'),
    url(r'^mes-projets/$', mes_projets, name='mes_projets'),
    url(r'^mes-projets/(?P<projet>\d+)/$', projet, name='projet'),
    url(r'^mes-projets/(?P<projet>\d+)/supprimer/$', supprimer_projet, name='supprimer_projet'),
    url(r'^mes-projets/(?P<projet>\d+)/update-donnees/$', update_donnees, name='update_donnees'),
    url(r'^profile/$', formulaire_profile, name='profile'),
    url(r'^profile/validation/$', valider_profile, name='valider_profile'),
    url(r'^profile/photo/$', photo, name='changer_photo'),
    url(r'^profile/photo/validation/$', valider_photo, name='valider_photo'),
    url(r'^profile/mot-de-passe/$', mot_de_passe, name='changer_mot_de_passe'),
    url(r'^profile/mot-de-passe/validation/$', valider_mot_de_passe, name='valider_mot_de_passe'),
    url(r'^supprimer-photo-profile/$', supprimer_photo, name='supprimer_photo'),
    url(r'^creation-projet/$', creation_projet, name='creation_projet'),
    url(r'^creation-projet/validation/$', valider_projet, name='valider_projet'),
    url(r'^importer-polygone/$', importer_polygone, name='importer_polygone'),
    url(r'^(?P<projet>\d+)/parcelle/$', creation_parcelle, name='creation_parcelle'),
    url(r'^(?P<projet>\d+)/parcelle/validation/$', valider_parcelle, name='valider_parcelle'),
    url(r'^(?P<projet>\d+)/sol/$', sol, name='sol'),
    url(r'^(?P<projet>\d+)/sol/validation/$', valider_sol, name='valider_sol'),
    url(r'^(?P<projet>\d+)/choix-sol/$', choix_sol, name='choix_sol'),
    url(r'^(?P<projet>\d+)/choix-sol/validation/$', valider_choix_sol, name='valider_choix_sol'),
    url(r'^(?P<projet>\d+)/plante/$', plante, name='plante'),
    url(r'^(?P<projet>\d+)/plante/validation/$', valider_plante, name='valider_plante'),
    url(r'^(?P<projet>\d+)/choix-plante/$', choix_plante, name='choix_plante'),
    url(r'^(?P<projet>\d+)/choix-plante/validation/$', valider_choix_plante, name='valider_choix_plante'),
    url(r'^(?P<projet>\d+)/noeud/$', noeud, name='noeud'),
    url(r'^(?P<projet>\d+)/noeud/validation/$', valider_noeud, name='valider_noeud'),
    url(r'^update-donnees/$', data_noeud, name='data_noeud')
]
