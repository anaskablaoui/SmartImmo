from django.contrib import admin
from .models import Proprietaire,Propriete
# Register your models here.
@admin.register(Proprietaire)
class ProprietaireAdmin(admin.ModelAdmin):
    list_display=('id','user','cin','telephone')

@admin.register(Propriete)
class ProprieteAdmin(admin.ModelAdmin):
    list_display=('id','nom','ville','adresse','proprietaire','etat')