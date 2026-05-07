from django.db import models
from Locataire.models import Locataire
from Proprietaire.models import Proprietaire,Propriete
from django.contrib.auth.models import AbstractUser, Group, Permission
from accounts.models import CustomUser

# Create your models here.

class Agents(models.Model):
    user      = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                                     related_name='agent')
    matricule = models.CharField(max_length=12, unique=True)
    cin       = models.CharField(max_length=10, unique=True)
    telephone = models.CharField(max_length=10, unique=True)

    class Meta:
        verbose_name        = 'Agent'
        verbose_name_plural = 'Agents'

    def __str__(self):
        return f"{self.user.nom} {self.user.prenom}"
class Baux(models.Model):
    #id=models.IntegerField(unique=True,primary_key=True)
    locataire=models.ForeignKey(Locataire,on_delete=models.CASCADE,null=False,related_name='Baux')
    agent=models.ForeignKey(Agents,on_delete=models.CASCADE,null=False,related_name='Baux')
    propriete=models.ForeignKey(Propriete,on_delete=models.CASCADE,null=False,related_name='Baux')
    proprietaire=models.ForeignKey(Proprietaire,on_delete=models.CASCADE,null=False,related_name='Baux')
    prix=models.DecimalField(max_digits=6,decimal_places=2)
    date_debut=models.DateField()
    date_sortie=models.DateField()

    def __str__(self):
        return f"Bail numéro {self.id}"
    
class Contrat(models.Model):
    id=models.IntegerField(unique=True,primary_key=True)
    agent=models.ForeignKey(Agents,on_delete=models.CASCADE,null=False,related_name='contrat')
    propriete=models.ForeignKey(Propriete,on_delete=models.CASCADE,null=False,related_name='contrat')
    pourcentage=models.DecimalField(max_digits=2,decimal_places=2)
    prix_min=models.DecimalField(max_digits=6,decimal_places=2)
    date_contrat=models.DateField()
    date_finContrat=models.DateField()

    def __str__(self):
        return f"Contrat numero {self.id}"
    
    
class Offre(models.Model):
    id=models.IntegerField(unique=True,primary_key=True)
    agent=models.ForeignKey(Agents,on_delete=models.CASCADE,null=False,related_name='offre')
    propriete=models.ForeignKey(Propriete,on_delete=models.CASCADE,null=False,related_name='offre')
    prix=models.DecimalField(max_digits=6,decimal_places=2)
    pourcentage=models.DecimalField(max_digits=5,decimal_places=2)
    date_offre=models.DateField()

    def __str__(self):
        return f"Offre numero {self.id}"
