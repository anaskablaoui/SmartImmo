from django.db import models
from accounts.models import CustomUser
from Proprietaire.models import Propriete

class Locataire(models.Model):
    user      = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                                     related_name='locataire')
    cin       = models.CharField(max_length=10, unique=True)
    telephone = models.CharField(max_length=10, unique=True)

    class Meta:
        verbose_name        = 'Locataire'
        verbose_name_plural = 'Locataires'

    def __str__(self):
        return f"{self.user.nom} {self.user.prenom}"
    
class Maintenance(models.Model):
    propriete=models.ForeignKey(Propriete,on_delete=models.CASCADE,related_name='Maintenance')
    description = models.CharField(max_length=250,null=False)
    locataire=models.ForeignKey(Locataire,on_delete=models.CASCADE,null=False)
    date=models.DateField()