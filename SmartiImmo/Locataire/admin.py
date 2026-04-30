from django.contrib import admin
from .models import Locataire
# Register your models here.

@admin.register(Locataire)
class LocataireAdmin(admin.ModelAdmin):
    list_display=('id','user','cin','telephone')