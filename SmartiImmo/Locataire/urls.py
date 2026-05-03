from django.urls import path
from .views import auth_view, home_View,logoutView

urlpatterns = [
    path("", auth_view, name="authLocataire"),
    path("home/", home_View, name="homeLocataire"),
     path('logout/', logoutView, name='logoutLoc')
]