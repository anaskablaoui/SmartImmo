
from django.urls import path
from .views import LoginView, homeView, logoutView,imprimer_baux,imprimer_contrat

urlpatterns = [
    path("", LoginView.as_view(), name="agentLogin"),
    path("home/", homeView, name="agentDashboard"),
    path("logout/", logoutView, name="agentLogout"),
    path("baux/<int:bail_id>/imprimer/", imprimer_baux, name="baux"),
    path("contrat/<int:contrat_id>/imprimer/", imprimer_contrat, name="contrat"),
]