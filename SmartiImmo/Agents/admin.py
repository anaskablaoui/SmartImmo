from django.contrib import admin
from .models import Agents,Baux,Contrat
# Register your models here.

@admin.register(Agents)
class AgentsAdmin(admin.ModelAdmin):
    list_display=('user','matricule','cin','telephone')

@admin.register(Baux)
class BauxAdmin(admin.ModelAdmin):
    list_display=('locataire','proprietaire','prix','date_debut','date_sortie')

@admin.register(Contrat)
class ContratAdmin(admin.ModelAdmin):
    list_display=('agent','propriete','pourcentage','prix_min','date_contrat','date_finContrat')