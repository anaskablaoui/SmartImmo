from django.urls import path
from .views import auth_view, homeView,logoutView,imprimer_contrat,imprimer_baux

urlpatterns = [
    path("", auth_view, name="auth"),
    path("home/", homeView, name="home"),
    path('logout/', logoutView, name='logout'),
    path('imprimer_contrat/<int:propriete_id>/', imprimer_contrat, name='imprimer_contrat'),
    path('imprimer_baux/<int:bail_id>/', imprimer_baux, name='imprimer_baux'),
]