from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView,DetailView
from accounts.models import CustomUser
from .forms import RegisterForm, LoginForm,ajoutProprieteForm,ContratForm
from .models import Proprietaire,Propriete
from Agents.models import Baux,Offre,Contrat
from Locataire.models import Maintenance
from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import TruncMonth
# Create your views here.
def auth_view(request):
    login_form    = LoginForm()
    register_form = RegisterForm()
    error         = None

    
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
                    role      = 'proprietaire',       
                )

                
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
def homeView(request,offre_id=None):
    proprietaire, created = Proprietaire.objects.get_or_create(user=request.user)
    proprietes = Propriete.objects.filter(proprietaire=proprietaire)
    baux=Baux.objects.filter(propriete__proprietaire=proprietaire)
    message=Maintenance.objects.filter(propriete__proprietaire__user=request.user)
    offre=Offre.objects.filter(propriete__proprietaire=proprietaire)
    form = ajoutProprieteForm()
    accepterForm=ContratForm()
    if request.method == 'POST':
        if offre_id:
            offre_instance = get_object_or_404(Offre, id=offre_id)
            Contrat.objects.create(
                agent        = offre_instance.agent,
                propriete    = offre_instance.propriete,
                prix_min        = offre_instance.prix,
                pourcentage   = offre_instance.pourcentage,
                date_contrat  = timezone.now(),
            )
            offre_instance.delete()
            messages.success(request, 'Offre acceptée avec succès.')
            return redirect('home')
        form = ajoutProprieteForm(request.POST, request.FILES)
        print("POST received")                    
        print(form.is_valid())                    
        print(form.errors)                        
        if form.is_valid():
            propriete = form.save(commit=False)
            propriete.proprietaire = proprietaire
            propriete.save()
            print("Saved!")                       
            return redirect('home')
    else:
        form = ajoutProprieteForm()

    baux_par_mois = (
    Baux.objects.filter(proprietaire=request.user.proprietaire)
    .annotate(mois=TruncMonth('date_debut'))
    .values('mois')
    .annotate(total_prix=Sum('prix'))
    .order_by('mois')
    )
    
    labels = [n['mois'].strftime('%B %Y') for n in baux_par_mois]
    data= [float(n['total_prix'])*0.3 for n in baux_par_mois]

    return render(request, 'home/index.html', {
        'proprietaire': proprietaire,
        'proprietes': proprietes,
        'ajoutPropriete': form,
        'baux':baux,
        'maintenances':message,
        'offres':offre,
        'chart_labels': labels,
        'chart_data':   data,
    })

def imprimer_contrat(request, propriete_id):
    propriete = get_object_or_404(Propriete, id=propriete_id)
    contrat = Contrat.objects.filter(propriete=propriete).first()
    return render(request, 'home/imprimer_contrat.html', {
        'propriete': propriete,
        'contrat': contrat
    })

def imprimer_baux(request, bail_id):
    bail = get_object_or_404(Baux, id=bail_id)
    return render(request, 'home/imprimer_baux.html', {
        'bail': bail
    })

class ContratDetailView(DetailView):
    model = Contrat
    template_name = 'home/imprimer_contrat.html'
    context_object_name = 'contrat'

    def get_queryset(self):
        return Contrat.objects.filter(propriete__proprietaire__user=self.request.user)
    
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
    

class OffreListView(ListView):
    model = Offre
    template_name = 'home/index.html'
    context_object_name = 'offres'

    def get_queryset(self):
        return Offre.objects.filter(propriete__proprietaire__user=self.request.user)
