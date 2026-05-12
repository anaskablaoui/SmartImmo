from django.db import models
from accounts.models import CustomUser
from Proprietaire.models import Propriete

class Locataire(models.Model):
    user      = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                                     related_name='locataire')
    cin       = models.CharField(max_length=10)
    telephone = models.CharField(max_length=10)

    class Meta:
        verbose_name        = 'Locataire'
        verbose_name_plural = 'Locataires'

    def __str__(self):
        return f"{self.user.nom} {self.user.prenom}"
    
class Maintenance(models.Model):
    titre=models.CharField(max_length=100)
    propriete=models.ForeignKey(Propriete,on_delete=models.CASCADE,related_name='Maintenance')
    description = models.CharField(max_length=250,null=False)
    locataire=models.ForeignKey(Locataire,on_delete=models.CASCADE,null=False)
    date=models.DateField()

    def __str__(self):
        return f"Maintenance pour {self.propriete} le {self.date}"

class demandeLocation(models.Model):
        propriete=models.ForeignKey(Propriete,on_delete=models.CASCADE,related_name='demandeLocation')
        prix=models.FloatField()
        date_entre=models.DateField()
        date_sortie=models.DateField()
        locataire=models.ForeignKey(Locataire,on_delete=models.CASCADE,null=False)
        dateDemande=models.DateField()

        def __str__(self):
            return f"Demande de location pour {self.propriete} le {self.dateDemande}"