from django.urls import path
from .views import auth_view


urlpatterns = [
    path("", auth_view, name="auth"),
]