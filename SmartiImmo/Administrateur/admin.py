from django.contrib import admin
from .models import Administrateur
# Register your models here.
@admin.register(Administrateur)
class Administrateuradmin(admin.ModelAdmin):
    list_display=('matricule','nom','prenom','password')
        