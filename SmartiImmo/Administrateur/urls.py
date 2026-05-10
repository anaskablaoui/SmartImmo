from django.urls import path
from . import views

# define a list of url patterns 
urlpatterns = [
    path('',views.LoginView.as_view(),name='adminLogin'),
    path('dashboard/',views.homeView,name='adminDashboard'),
    path('logout/',views.logoutView,name='adminLogout'),
    path('supprimerAgent/<int:agent_id>/', views.supprimerAgent, name='adminSupprimAgent')
]