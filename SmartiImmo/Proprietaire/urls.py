from django.urls import path
from .views import auth_view, homeView,logoutView,imprimer_contrat,imprimer_baux,supprimerPropriete

urlpatterns = [
    path("", auth_view, name="auth"),
    path("home/", homeView, name="home"),
    path('logout/', logoutView, name='logout'),
    path('imprimer_contrat/<int:propriete_id>/', imprimer_contrat, name='imprimer_contrat'),
    path('imprimer_baux/<int:bail_id>/', imprimer_baux, name='imprimer_baux'),
    path('accepter_offre/<int:offre_id>/', homeView, name='accepter_offre'),
    path('supprimer_propriete/<int:propriete_id>/',supprimerPropriete,name='supprimerPropriete')
]