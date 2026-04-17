from django.contrib import admin
from .models import Agents,Baux,Contrat
# Register your models here.

@admin.register(Agents)
class AgentsAdmin(admin.ModelAdmin):
    list_display=('matricule','nom','prenom','CIN','password','telephone','email')

@admin.register(Baux)
class BauxAdmin(admin.ModelAdmin):
    liste_display=('locataire','proprietaire','prix','date_debut','debut_sortie')

@admin.register(Contrat)
class ContratAdmin(admin.ModelAdmin):
    list_display=('agent','propriete','pourcentage','prix_min','date_contrat','date_finContrat')