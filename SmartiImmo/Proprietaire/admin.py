from django.contrib import admin
from .models import Proprietaire,Propriete
# Register your models here.
@admin.register(Proprietaire)
class ProprietaireAdmin(admin.ModelAdmin):
    list_display=('id','email','nom','prenom','Cin','Telephone','password')

@admin.register(Propriete)
class ProprieteAdmin(admin.ModelAdmin):
    list_display=('id','ville','adresse','proprietaire','etat')