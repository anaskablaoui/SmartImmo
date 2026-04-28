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
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'input'
    }))
    password_confirm=forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'input'
    }))
    class Meta:
        model=Proprietaire
        fields = ['nom','prenom','email','password','password_confirm']
    
    def clean(self):
        self.cleaned_data=super().clean()
        self.cleaned_data=self.cleaned_data.get('prenom')
        self.cleaned_data=self.cleaned_data.get('nom')
        self.password=self.cleaned_data.get('password')
        self.password_confirm=self.cleaned_data.get('password_confirm')
        #check if the password match 
        if self.password and self.password_confirm and self.password != self.password_confirm:
            raise forms.ValidationError(f"password does not match ")
        return self.cleaned_data
        

class LoginForm(forms.ModelForm):
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

    