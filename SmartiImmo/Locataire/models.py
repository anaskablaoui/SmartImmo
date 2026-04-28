from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission
# Create your models here.

class Locataire(AbstractUser):
    username = None  # Désactiver le username par défaut
    
    id = models.IntegerField(unique=True, primary_key=True)
    email = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=20, unique=False)
    prenom = models.CharField(max_length=20, unique=False)
    Cin = models.CharField(max_length=10, unique=True)
    Telephone = models.CharField(max_length=10, unique=True)
    # password est déjà dans AbstractUser - ne pas le déclarer
    
    USERNAME_FIELD = 'email'  # Utiliser email pour l'authentification
    REQUIRED_FIELDS = ['nom', 'prenom', 'Cin', 'Telephone']
    
    class Meta:
        verbose_name = 'Locataire'
        verbose_name_plural = 'Locataires'
    
    groups = models.ManyToManyField(
        Group,
        related_name="locataire_groups",
        related_query_name="locataire",
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.'
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="locataire_permissions",
        related_query_name="locataire",
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.'
    )
    
    def __str__(self):
        return f"{self.nom} {self.prenom}"
