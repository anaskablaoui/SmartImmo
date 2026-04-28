from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission
# Create your models here.
class Administrateur(AbstractUser):
    username = None  # Désactiver le username par défaut
    
    matricule = models.CharField(max_length=12, unique=True, primary_key=True)
    nom = models.CharField(max_length=50, unique=False)
    prenom = models.CharField(max_length=50, unique=False)
    email = models.CharField(max_length=50, unique=True)
    # password est déjà dans AbstractUser - ne pas le déclarer
    
    USERNAME_FIELD = 'matricule'  # Utiliser matricule pour l'authentification
    REQUIRED_FIELDS = ['email', 'nom', 'prenom']
    
    class Meta:
        verbose_name = 'Administrateur'
        verbose_name_plural = 'Administrateurs'
    
    groups = models.ManyToManyField(
        Group,
        related_name="administrateur_groups",
        related_query_name="administrateur",
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.'
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="administrateur_permissions",
        related_query_name="administrateur",
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.'
    )
    
    def __str__(self):
        return f"{self.nom} {self.prenom}"


