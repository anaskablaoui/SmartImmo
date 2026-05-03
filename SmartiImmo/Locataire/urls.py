from django.urls import path
from .views import auth_view, homeView,logoutView

urlpatterns = [
    path("", auth_view, name="authLocataire"),
    path("home/", homeView, name="homeLocataire"),
     path('logout/', logoutView, name='logout')
]