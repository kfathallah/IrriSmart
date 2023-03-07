from serveur.settings import MEDIA_URL, MEDIA_ROOT, DEBUG
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.conf.urls import url, include
from application.views import erreur
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns=[
    url(r'^application/', include('application.urls',namespace="application")),
    url(r'^admin/', admin.site.urls)
]+static(MEDIA_URL, document_root=MEDIA_ROOT)

urls_utilisateur_inaccessibles=[
    '/application/',
    '/application/inscription/',
    '/application/inscription/validation/',
    '/application/connexion/',
    '/application/connexion/validation/',
    '/application/envoyer-message/',
    '/'
]

urls_accessibles=['/application/deconnexion/']+urls_utilisateur_inaccessibles

handler404=erreur.erreur404

handler500=erreur.erreur500

if settings.DEBUG==False:
    import django
    urlpatterns+=[
        url(r'^media/(?P<path>.*)$', django.views.static.serve, {'document_root': settings.MEDIA_ROOT}),
        url(r'^static/(?P<path>.*)$', django.views.static.serve, {'document_root': settings.STATIC_ROOT})
    ]
