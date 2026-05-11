from django.utils import timezone

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView
from accounts.models import CustomUser
from .forms import RegisterForm, LoginForm, demandeLocationForm,demandeMaintenanceForm,demandeLocation
from .models import Locataire,Maintenance
from Agents.models import Contrat,Baux
from Proprietaire.models import Propriete

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
def home_View(request):
    locataire_obj , _=Locataire.objects.get_or_create(user=request.user)
    contrat = Contrat.objects.all()
    return render(request, 'locataire/index.html', {
        'locataire': locataire_obj,
        'contrats': contrat
    })

@login_required
def historique_view(request):
    locataire_obj, _ = Locataire.objects.get_or_create(user=request.user)
    history = Baux.objects.filter(locataire__user=request.user)
    return render(request, 'locataire/history.html', {
        'locataire': locataire_obj,
        'baux':history
    })

@login_required
def maintenance_view(request):
    locataire_obj, _ = Locataire.objects.get_or_create(user=request.user)
    proprietes_locataire = Propriete.objects.filter(Baux__locataire=locataire_obj).distinct()
    maintenances = Maintenance.objects.filter(locataire__user=request.user)
    if request.method == 'POST':
        form = demandeMaintenanceForm(request.POST)
        form.fields['propriete'].queryset = proprietes_locataire
        if form.is_valid():
            maintenance = form.save(commit=False)
            maintenance.locataire = locataire_obj
            maintenance.status = 'en attente'
            maintenance.date=timezone.now().date()
            maintenance.save()
            messages.success(request, "Demande de maintenance soumise avec succès.")
            return redirect('maintenanceLoc')
    else:                                  
        form = demandeMaintenanceForm()
        form.fields['propriete'].queryset = proprietes_locataire

    locataire_obj, _ = Locataire.objects.get_or_create(user=request.user)
    return render(request, 'locataire/maintenance.html', {
        'locataire': locataire_obj,
        'form': form,
        'maintenances': maintenances
    })

def imprimerBaux(request, bail_id):
    bail = get_object_or_404(Baux, id=bail_id)
    return render(request, 'locataire/locatairebaux.html', {
        'bail': bail
    })


def demandelocationView(request,contrat_id):
    contrat = get_object_or_404(Contrat,id=contrat_id)
    if request.method == 'POST':
        form=demandeLocationForm(request.POST)
        if form.is_valid():
            demande=form.save(commit=False)
            demande.propriete=contrat.propriete
            demande.dateDemande=timezone.now().date()
            demande.locataire=Locataire.objects.get(user=request.user)
            demande.save()
            messages.success(request, "Demande de location soumise avec succès.")
            return redirect('homeLocataire')
        
    else:
        form=demandeLocationForm()

    return render(request,'locataire/demandeLocation.html',{
        'form':form,
        'appartement':contrat
        })
    


class proprieteListView(ListView):
    model = Contrat
    template_name = 'locataire/index.html'
    context_object_name = 'contrats'

class historiqueListView(ListView):
    model = Baux
    template_name = 'locataire/history.html'
    context_object_name = 'baux'

    def get_queryset(self):
        return Baux.objects.filter(locataire__user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now().date()
        return context
    
class MaintenanceListView(ListView):
    model = Maintenance
    template_name = 'locataire/maintenance.html'
    context_object_name = 'maintenances'

    def get_queryset(self):
        return Maintenance.objects.filter(locataire__user=self.request.user)