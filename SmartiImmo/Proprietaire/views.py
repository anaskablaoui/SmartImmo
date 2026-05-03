from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView,DetailView
from accounts.models import CustomUser
from .forms import RegisterForm, LoginForm,ajoutProprieteForm
from .models import Proprietaire,Propriete
from Agents.models import Baux
from Locataire.models import Maintenance


def auth_view(request):
    login_form    = LoginForm()
    register_form = RegisterForm()
    error         = None

    # Déjà connecté = redirection directe
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        # LOGIN
        if form_type == 'login':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                email    = login_form.cleaned_data['email']
                password = login_form.cleaned_data['password']

                user = authenticate(request, username=email, password=password)

                if user is not None and user.role == 'proprietaire':
                    login(request, user)
                    return redirect('home')
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
                    role      = 'proprietaire',       # rôle fixé automatiquement
                )

                # 2. Compléter le profil Proprietaire (signal crée la ligne,
                #    on met à jour les champs spécifiques)
                proprietaire, _ = Proprietaire.objects.get_or_create(user=user)
                proprietaire.cin       = data['cin']
                proprietaire.telephone = data['telephone']
                proprietaire.save()

                # 3. Connecter et rediriger
                login(request, user)
                return redirect('home')
            else:
                error = "Veuillez corriger les erreurs du formulaire."

    return render(request, 'accounts/index.html', {
        'loginForm':    login_form,
        'registerForm': register_form,
        'error':        error,
    })


def logoutView(request):
    if request.method == 'POST':
        logout(request)
        return redirect('auth')
    return redirect('home')


@login_required(login_url='/proprietaire/')
def homeView(request):
    proprietaire, created = Proprietaire.objects.get_or_create(user=request.user)
    proprietes = Propriete.objects.filter(proprietaire=proprietaire)

    if request.method == 'POST':
        form = ajoutProprieteForm(request.POST, request.FILES)
        print("POST received")                    # ← check 1
        print(form.is_valid())                    # ← check 2
        print(form.errors)                        # ← check 3: shows why invalid
        if form.is_valid():
            propriete = form.save(commit=False)
            propriete.proprietaire = proprietaire
            propriete.save()
            print("Saved!")                       # ← check 4
            return redirect('home')
    else:
        form = ajoutProprieteForm()

    return render(request, 'home/index.html', {
        'proprietaire': proprietaire,
        'proprietes': proprietes,
        'ajoutPropriete': form,
    })
class ProprieteListView(ListView):
    model = Proprietaire
    template_name = 'home/index.html'
    context_object_name = 'proprietes'
    
    # avoir juste les propriete de proprietaire connecté
    def get_queryset(self):
        return Propriete.objects.filter(user=self.request.user)

# je dois ajouter les details de la propriete pour les afficher dans la page d'accueil
class ProprieteDetailView(DetailView):
    pass

class BauxListeView(ListView):
    model = Baux
    template_name = 'home/index.html'
    context_object_name = 'baux'
    
    #avoir les baux de proprietaire connecté
    def get_queryset(self):
        return Baux.objects.filter(user=self.request.user)
    
class MessageListeView(ListView):
    model=Maintenance
    template_name='home/index.html'
    context_object_name='maintenances'

    def get_queryset(self):
        return Maintenance.objects.filter(propriete__proprietaire__user=self.request.user)