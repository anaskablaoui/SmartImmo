from django import forms
from accounts.models import CustomUser
from .models import Locataire,Maintenance


class RegisterForm(forms.Form):
    nom = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input',
        'placeholder': 'Entrer nom'
    }))
    prenom = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input',
        'placeholder': 'Entrer prénom'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'input',
        'placeholder': 'Entrer email'
    }))
    cin = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input',
        'placeholder': 'Entrer CIN'
    }))
    telephone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input',
        'placeholder': 'Entrer téléphone'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'input',
        'placeholder': 'Entrer mot de passe'
    }))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'input',
        'placeholder': 'Confirmer mot de passe'
    }))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé.")
        return email

    def clean_cin(self):
        cin = self.cleaned_data.get('cin')
        if Locataire.objects.filter(cin=cin).exists():
            raise forms.ValidationError("Ce CIN est déjà utilisé.")
        return cin

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")

        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'input',
        'placeholder': 'Entrer email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'input',
        'placeholder': 'Entrer mot de passe'
    }))


class demandeMaintenanceForm(forms.ModelForm):
    titre = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input',
        'placeholder': 'Titre de la maintenance'
    }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-input',
        'placeholder': 'Décrire le problème',
        'rows': 4
    }))

    class Meta:
        model = Maintenance
        fields = ['titre', 'description']