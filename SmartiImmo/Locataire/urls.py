from django.urls import path
from .views import auth_view, home_View,logoutView,historique_view, maintenance_view,imprimerBaux,demandelocationView

urlpatterns = [
    path("", auth_view, name="authLocataire"),
    path("home/", home_View, name="homeLocataire"),
    path('logout/', logoutView, name='logoutLoc'),
    path('history/', historique_view, name='historyLoc'),
    path('maintenance/', maintenance_view, name='maintenanceLoc'),
    path("baux/<int:bail_id>/imprimer/", imprimerBaux, name="locbaux"),
    path("demandelocation/<int:contrat_id>",demandelocationView,name="demandelocation")
]