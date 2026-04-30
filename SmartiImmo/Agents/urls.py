
from django.urls import path
from .views import LoginView, homeView

urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("home/", homeView, name="home"),
    
   
]