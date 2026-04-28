from django import forms
from .models import Proprietaire

class RegisterForm(forms.ModelForm):
    nom=forms.CharField(widget=forms.TextInput(attrs={
        'class':'input',
        'placeholder':'enter nom'
    }))
    prenom=forms.CharField(widget=forms.TextInput(attrs={
        'class':'input',
        'placeholder':'entrer password'
    }))
    email=forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'input',
        'placeholder':'entrer email'
    }))
    password=forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model=Proprietaire
        fields = ['nom','prenom','password']

class LoginForm(forms.ModelForm):
