from django import forms
from .models import Administrateur
from accounts.models import CustomUser
from Agents.models import Agents


class adminLoginForm(forms.ModelForm):
    email=forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class':'form-input',
            'placeholder':'entrer email'
        }
    ))
    password=forms.CharField(widget=forms.PasswordInput(
        attrs={
        'class':'form-input',
        'placeholder':'entrer password',
        
    }))
    
    class Meta:
        model= Administrateur
        fields = ['email','password']

class AdministrateurCreationForm(forms.ModelForm):
    # Champs du CustomUser à remplir
    nom= forms.CharField(label="Nom")
    prenom= forms.CharField(label="Prénom")
    email = forms.EmailField(label="Email", required=False)
    password1 = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmer le mot de passe", widget=forms.PasswordInput)

    class Meta:
        model = Administrateur
        fields = ['matricule']  # sans 'user'

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data


    def save(self, commit=True):
        # Créer le CustomUser avec le rôle 'agent'
        user = CustomUser.objects.create_user(
            nom=self.cleaned_data['nom'],
            prenom=self.cleaned_data['prenom'],
            email=self.cleaned_data.get('email', ''),
            matricule=self.cleaned_data['matricule'],
            password=self.cleaned_data['password1'],
            role='administrateur'  # 👈 adapte selon ton champ role dans CustomUser
        )
        administrateur = super().save(commit=False)
        administrateur.user = user
        if commit:
            administrateur.save()
        return administrateur

class AjoutAgentForm(forms.ModelForm):
    nom       = forms.CharField(label="Nom")
    prenom    = forms.CharField(label="Prénom")
    email     = forms.EmailField(label="Email")
    password1 = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmer", widget=forms.PasswordInput)

    class Meta:
        model  = Agents
        fields = ['matricule', 'cin', 'telephone']

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data
    
    def save(self, commit=True):
        user = CustomUser(
            nom    = self.cleaned_data['nom'],
            prenom = self.cleaned_data['prenom'],
            email  = self.cleaned_data['email'],
            role   = 'agent',
        )
        user.set_password(self.cleaned_data['password1'])
        user.save()

        agent = super().save(commit=False)
        agent.user = user
        if commit:
            agent.save()
        return agent