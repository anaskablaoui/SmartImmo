from django.urls import path
from .views import auth_view, homeView,logoutView

urlpatterns = [
    path("", auth_view, name="auth"),
    path("home/", homeView, name="home"),
     path('logout/', logoutView, name='logout')
]