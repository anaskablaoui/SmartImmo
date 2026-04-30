from django.db import models
from accounts.models import CustomUser


class Administrateur(models.Model):
    user      = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                                     related_name='administrateur')
    matricule = models.CharField(max_length=12, unique=True)

    class Meta:
        verbose_name        = 'Administrateur'
        verbose_name_plural = 'Administrateurs'

    def __str__(self):
        return f"{self.user.nom} {self.user.prenom}"