from django.contrib import admin
from .models import Locataire, Maintenance
# Register your models here.

@admin.register(Locataire)
class LocataireAdmin(admin.ModelAdmin):
    list_display=('id','user','cin','telephone')

@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display=('id','titre','locataire','date')