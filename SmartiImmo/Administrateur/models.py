from django.db import models

# Create your models here.
class Administrateur(models.Model):
    matricule=models.CharField(max_length=12,unique=True,primary_key=True)
    nom=models.CharField(max_length=50,unique=False)
    prenom=models.CharField(max_length=50,unique=False)
    password=models.CharField(max_length=20)

    def __str__(self):
        return self.name
