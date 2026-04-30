from django.db import models
from accounts.models import CustomUser


class Proprietaire(models.Model):
    user      = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                                     related_name='proprietaire')
    cin       = models.CharField(max_length=10)
    telephone = models.CharField(max_length=10)

    class Meta:
        verbose_name        = 'Propriétaire'
        verbose_name_plural = 'Propriétaires'

    def __str__(self):
        return f"{self.user.nom} {self.user.prenom}"


class Propriete(models.Model):
    ville        = models.CharField(max_length=50)
    adresse      = models.CharField(max_length=250, unique=True)
    proprietaire = models.ForeignKey(Proprietaire, on_delete=models.CASCADE,
                                     related_name='proprietes')
    etat         = models.CharField(max_length=250)
    image        = models.ImageField(null=True, blank=True, upload_to='Proprietaire/')

    def __str__(self):
        return f"Propriété : {self.adresse}"