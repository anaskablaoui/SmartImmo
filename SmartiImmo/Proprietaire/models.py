from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser,Group,Permission

class ProprietaireManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)


# Create your models here.
class Proprietaire(AbstractUser):
    username = None
    
    
    email=models.EmailField(max_length=50,unique=True)
    nom=models.CharField(max_length=20,unique=False)
    prenom=models.CharField(max_length=20,unique=False)
    Cin=models.CharField(max_length=10)
    Telephone=models.CharField(max_length=10)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[]
    objects = ProprietaireManager()

    class Meta:
        verbose_name= 'Proprietaire'
        verbose_name_plural='Proprietaire'
    
    groups = models.ManyToManyField(
        Group,
        related_name="proprietaire_groups",
        related_query_name="proprietauire",
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to .'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="proprietaire_permissions",
        related_query_name="proprietaire",
        blank=True,
        verbose_name='proprietaire permssion',
        help_text='soecufu permissions for this user.'
    )
    def __str__(self):
        return f"{self.nom} {self.prenom}" if self.nom and self.prenom else self.email
    
class Propriete(models.Model):
    
    ville=models.CharField(max_length=50,unique=False)
    adresse=models.CharField(max_length=250,unique=True)
    proprietaire=models.ForeignKey(Proprietaire,on_delete=models.CASCADE,null=False,related_name='propriete')
    etat=models.CharField(max_length=250,unique=False)
    image=models.ImageField(null=True,upload_to='Proprietaire/')

    def __str__(self):
        return "suppression de propriete addresse:"+self.adresse

    