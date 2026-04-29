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
    cin=forms.CharField(widget=forms.TextInput(attrs={
        'class':'input',
        'placeholder':'entrer CIN'
    }))
    email=forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'input',
        'placeholder':'entrer email'
    }))
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'input'
    }))
    password_confirm=forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'input'
    }))
    class Meta:
        model=Proprietaire
        fields = ['nom','prenom','email','cin','password','password_confirm']
    
    def clean(self):
        cleaned_data = super().clean()  
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")

        return cleaned_data  
        

class LoginForm(forms.Form):
    email=forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'input',
        'placeholder':'entrer email'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'input',
        'placeholder':'entrer password'
    }))

    class Meta:
        model=Proprietaire
        fields= ['email','password']

    