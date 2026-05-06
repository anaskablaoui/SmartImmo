
from django.urls import path
from .views import LoginView, homeView, logoutView

urlpatterns = [
    path("", LoginView.as_view(), name="agentLogin"),
    path("home/", homeView, name="agentDashboard"),
    path("logout/", logoutView, name="agentLogout"),
]