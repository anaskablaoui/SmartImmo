from django.db import models
from Locataire.models import Locataire
from Proprietaire.models import Proprietaire,Propriete
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.

class Agents(AbstractUser):

    username = None  
    matricule = models.CharField(max_length=12, unique=True, primary_key=True)
    nom = models.CharField(max_length=50, unique=False)
    prenom = models.CharField(max_length=50, unique=False)
    CIN = models.CharField(max_length=10, unique=True)
    telephone = models.CharField(max_length=10, unique=True)

    USERNAME_FIELD = 'matricule'
    REQUIRED_FIELDS = ['email', 'nom', 'prenom', 'CIN', 'telephone']  # Champs requis pour createsuperuser
    
    class Meta:
        verbose_name = 'Agent'
        verbose_name_plural = 'Agents'
    
    # Redéfinir les relations ManyToMany pour éviter les conflits
    groups = models.ManyToManyField(
        Group,
        related_name="agents_groups",
        related_query_name="agent",
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.'
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="agents_permissions",
        related_query_name="agent",
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.'
    )
    
    def __str__(self):
        return f"{self.nom} {self.prenom}"
class Baux(models.Model):
    id=models.IntegerField(unique=True,primary_key=True)
    locataire=models.ForeignKey(Locataire,on_delete=models.CASCADE,null=False,related_name='Baux')
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
    