from django.db import models

# Create your models here.
class Locataire(models.Model):
    id=models.IntegerField(unique=True,primary_key=True)
    email=models.CharField(max_length=50,unique=True)
    nom=models.CharField(max_length=20,unique=False)
    prenom=models.CharField(max_length=20,unique=False)
    Cin=models.CharField(max_length=10,unique=True)
    Telephone=models.CharField(max_length=10,unique=True)
    password=models.CharField(max_length=20,unique=False)

    def __str__(self):
        return self.nom
    
