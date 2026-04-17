from django.db import models

# Create your models here.
class Proprietaire(models.Model):
    id=models.IntegerField(unique=True,primary_key=True)
    email=models.CharField(max_length=50,unique=True)
    nom=models.CharField(max_length=20,unique=False)
    prenom=models.CharField(max_length=20,unique=False)
    Cin=models.CharField(max_length=10,unique=True)
    Telephone=models.CharField(max_length=10,unique=True)
    password=models.CharField(max_length=20,unique=False)

    def __str__(self):
        return self.name
    
class Propriete(models.Model):
    id=models.IntegerField(unique=True,primary_key=True)
    ville=models.CharField(max_length=50,unique=False)
    adresse=models.CharField(max_length=250,unique=True)
    proprietaire=models.ForeignKey(Proprietaire,on_delete=models.CASCADE,null=False,related_name='propriete')
    etat=models.CharField(max_length=250,unique=False)
    image=models.ImageField(null=True,upload_to='Proprietaire/')

    def __str__(self):
        return "suppression de propriete addresse:"+self.adresse

    