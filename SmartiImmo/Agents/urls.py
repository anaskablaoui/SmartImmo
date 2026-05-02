
from django.urls import path
from .views import LoginView, homeView, logoutView

urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("home/", homeView, name="dashboard"),
    path("logout/", logoutView, name="logout"),
    
   
]