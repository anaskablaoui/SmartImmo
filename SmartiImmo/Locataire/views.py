from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.models import CustomUser
from .forms import RegisterForm, LoginForm
from .models import Locataire


def auth_view(request):
    login_form    = LoginForm()
    register_form = RegisterForm()
    error         = None

    # Déjà connecté = redirection directe
    if request.user.is_authenticated:
        return redirect('homeLocataire')

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        # LOGIN
        if form_type == 'login':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                email    = login_form.cleaned_data['email']
                password = login_form.cleaned_data['password']

                user = authenticate(request, username=email, password=password)

                if user is not None and user.role == 'locataire':
                    login(request, user)
                    return redirect('homeLocataire')
                else:
                    error = "Email ou mot de passe incorrect."

        # REGISTER
        elif form_type == 'register':
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                data = register_form.cleaned_data

                # 1. Créer le CustomUser
                user = CustomUser.objects.create_user(
                    email     = data['email'],
                    password  = data['password'],
                    nom       = data['nom'],
                    prenom    = data['prenom'],
                    role      = 'locataire',       # rôle fixé automatiquement
                )

                # 2. Compléter le profil Proprietaire (signal crée la ligne,
                #    on met à jour les champs spécifiques)
                locataire, _ = Locataire.objects.get_or_create(user=user)
                locataire.cin       = data['cin']
                locataire.telephone = data['telephone']
                locataire.save()

                # 3. Connecter et rediriger
                login(request, user)
                return redirect('homeLocataire')
            else:
                error = "Veuillez corriger les erreurs du formulaire."

    return render(request, 'locataire_accounts/index.html', {
        'loginForm':    login_form,
        'registerForm': register_form,
        'error':        error,
    })


def logoutView(request):
    if request.method == 'POST':
        logout(request)
        return redirect('authLocataire')
    return redirect('homeLocataire')


@login_required
def homeView(request):
    locataire_obj, _ = Locataire.objects.get_or_create(user=request.user)
    return render(request, 'locataire/index.html', {
        'locataire': locataire_obj
    })