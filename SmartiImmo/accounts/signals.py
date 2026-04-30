from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from Administrateur.models import Administrateur
from Agents.models import Agents
from Locataire.models import Locataire
from Proprietaire.models import Proprietaire


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if not created:
        return

    profiles = {
        'administrateur': lambda: Administrateur.objects.create(
            user=instance, matricule=instance.matricule or ''
        ),
        'agent': lambda: Agents.objects.create(
            user=instance, matricule=instance.matricule or '',
            cin='', telephone=''
        ),
        'locataire': lambda: Locataire.objects.create(
            user=instance, cin='', telephone=''
        ),
        'proprietaire': lambda: Proprietaire.objects.create(
            user=instance, cin='', telephone=''
        ),
    }

    creator = profiles.get(instance.role)
    if creator:
        creator()