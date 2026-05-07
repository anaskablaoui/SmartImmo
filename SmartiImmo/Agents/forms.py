
from django import forms
from .models import Agents, Baux
from accounts.models import CustomUser
from Agents.models import Offre
# 1. Formulaire custom pour créer un Agent + son User en même temps
class AgentCreationForm(forms.ModelForm):
    # Champs du CustomUser à remplir
    nom= forms.CharField(label="Nom")
    prenom= forms.CharField(label="Prénom")
    email = forms.EmailField(label="Email", required=False)
    password1 = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmer le mot de passe", widget=forms.PasswordInput)

    class Meta:
        model = Agents
        fields = ('matricule', 'cin', 'telephone')  # sans 'user'

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
            role='agent'  # 👈 adapte selon ton champ role dans CustomUser
        )
        agent = super().save(commit=False)
        agent.user = user
        if commit:
            agent.save()
        return agent


# 2. Formulaire pour la modification (garde le user existant)
class AgentChangeForm(forms.ModelForm):
    class Meta:
        model = Agents
        fields = '__all__'



class loginForm(forms.ModelForm):
    email=forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'input',
        'placeholder':'entrer email',
        
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'input',
        'placeholder':'entrer password',
        
    }))

    class Meta:
        model= Agents
        fields= ['email','password']

class bauxForm(forms.ModelForm):
    locataire=forms.CharField(widget=forms.TextInput(attrs={
        'class':'input',
        'placeholder':'Nom du locataire',
        'placeholder':'Prénom du locataire'
    }))
    propriete=forms.CharField(widget=forms.TextInput(attrs={
        'class':'input',
        'placeholder':'Adresse de la propriété'
    }))
    prix=forms.DecimalField(widget=forms.NumberInput(attrs={
        'class':'input',    
        'placeholder':'Prix du bail'
    }))
    date_debut=forms.DateField(widget=forms.DateInput(attrs={
        'class':'input',
        'placeholder':'Date de début',
        'type':'date'
    }))
    date_sortie=forms.DateField(widget=forms.DateInput(attrs={
        'class':'input',
        'placeholder':'Date de sortie',
        'type':'date'
    }))

    
    class Meta:
        model = Baux
        fields = '__all__'

class accepterlocationForm(forms.ModelForm):
    
    class Meta:
        model = Baux
        fields = []
        
class ContratForm(forms.ModelForm):
    prix=forms.DecimalField(widget=forms.NumberInput(attrs={
        'class':'input',
        'placeholder':'Prix du contrat'
    }))
    pourcentage=forms.DecimalField(widget=forms.NumberInput(attrs={
        'class':'input',
        'placeholder':'Pourcentage du contrat'
    }))
    class Meta:
        model = Offre
        fields = ['prix','pourcentage']