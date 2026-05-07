from django.contrib import admin
from .models import Agents,Baux,Contrat,Offre
from django.contrib.auth import get_user_model
from .forms import AgentCreationForm, AgentChangeForm
# Register your models here.
CustomUser = get_user_model()

@admin.register(Agents)
class AgentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'matricule', 'cin', 'telephone')

    def get_form(self, request, obj=None, **kwargs):
      
        if obj is None:
            kwargs['form'] = AgentCreationForm
        else:
            kwargs['form'] = AgentChangeForm
        return super().get_form(request, obj, **kwargs)

    def get_fields(self, request, obj=None):
        if obj is None:
            
            return ('nom', 'prenom', 'email', 'password1', 'password2', 'matricule', 'cin', 'telephone')
        else:
           
            return ('user', 'matricule', 'cin', 'telephone')


@admin.register(Baux)
class BauxAdmin(admin.ModelAdmin):
    list_display = ('locataire', 'proprietaire', 'prix', 'date_debut', 'date_sortie')

@admin.register(Contrat)
class ContratAdmin(admin.ModelAdmin):
    list_display = ('agent', 'propriete', 'pourcentage', 'prix_min', 'date_contrat', 'date_finContrat')

@admin.register(Offre)
class OffreAdmin(admin.ModelAdmin):
    list_display = ('agent', 'propriete', 'prix', 'pourcentage', 'date_offre')