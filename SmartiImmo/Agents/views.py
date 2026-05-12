from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import loginForm,accepterlocationForm,ContratForm
from .models import Agents,Baux,Contrat
from django.contrib import messages
from django.views.generic import ListView,DetailView
from Locataire.models import Maintenance
from Proprietaire.models import Propriete
from Locataire.models import demandeLocation
from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import TruncMonth
import json
# Create your views here.
class LoginView(View):
    def get(self, request):
        form = loginForm()
        return render(request, 'login/index.html', {'form': form})

    def post(self, request):
        form = loginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('agentDashboard')
            else:
                messages.error(request, 'Invalid email or password.')
        return render(request, 'login/index.html', {'form': form})

def logoutView(request):
    if request.method == 'POST':
        logout(request)
        return redirect('agentLogin')
    return redirect('agentDashboard')

@login_required(login_url='/agent/')
def homeView(request, offre_id=None, propriete_id=None):
    offreForm = ContratForm()

    if request.method == 'POST':
        print("offre_id:", offre_id)
        print("propriete_id:", propriete_id)

        if offre_id:
            demande = get_object_or_404(demandeLocation, id=offre_id)
            Baux.objects.create(
                locataire    = demande.locataire,
                agent        = request.user.agent,
                propriete    = demande.propriete,
                proprietaire = demande.propriete.proprietaire,
                prix         = demande.prix,
                date_debut   = demande.date_entre,
                date_sortie  = demande.date_sortie,
            )
            demande.delete()
            messages.success(request, 'Location acceptée avec succès.')
            return redirect('agentDashboard')

        elif propriete_id:
            offreForm = ContratForm(request.POST)
            if offreForm.is_valid():
                print("form valid:", offreForm.is_valid())
                print("form errors:", offreForm.errors)
                print("POST data:", request.POST)
                instance = offreForm.save(commit=False)
                instance.agent = request.user.agent
                instance.propriete = get_object_or_404(Propriete, id=propriete_id)
                instance.date_offre = timezone.now()
                instance.save()
                messages.success(request, 'offre est envoye et  créé avec succès.')
                return redirect('agentDashboard')
            else:
                print("Erreurs:", offreForm.errors)
    baux_par_mois = (
    Baux.objects.filter(agent=request.user.agent)
    .annotate(mois=TruncMonth('date_debut'))
    .values('mois')
    .annotate(total_prix=Sum('prix'))
    .order_by('mois')
    )
    
    labels = [n['mois'].strftime('%B %Y') for n in baux_par_mois]
    data= [float(n['total_prix'])*0.3 for n in baux_par_mois]

    return render(request, 'home/home.html', {
        'agent':       request.user.agent,
        'demandes':     demandeLocation.objects.all(),
        'maintenances': Maintenance.objects.filter(propriete__contrat__agent=request.user.agent).distinct(),
        'contrats':     Contrat.objects.filter(agent=request.user.agent),
        'Baux':         Baux.objects.filter(agent=request.user.agent),
        'proprietes':   Propriete.objects.all(),
        'offreForm':    offreForm,
        'chart_labels': labels,
        'chart_data':   data,
    })      
def imprimer_baux(request, bail_id):
    bail = get_object_or_404(Baux, id=bail_id)
    return render(request, 'home/baux.html', {
        'bail': bail
    })

def supprimerOffreLocation(request,demandeLocation_id):
    demande=get_object_or_404(demandeLocation,id=demandeLocation_id)
    demande.delete()
    return redirect('agentDashboard')

def imprimer_contrat(request, contrat_id):
    contrat = get_object_or_404(Contrat, id=contrat_id)
    return render(request, 'home/contrat.html', {
        'contrat': contrat})


class BauxListView(ListView):
    model = Baux
    template_name = 'home/index.html'
    context_object_name = 'Baux'
    
    # avoir juste les propriete de proprietaire connecté
    def get_queryset(self):
        return Baux.objects.filter(agent=self.request.user.agent)
    
class BauxDetailView(DetailView):
    model = Baux
    template_name = 'home/baux_detail.html'
    context_object_name = 'bail'
    
class ContratListView(ListView):
    model = Contrat
    template_name = 'home/index.html'
    context_object_name = 'contrats'
    
    # avoir juste les propriete de proprietaire connecté
    def get_queryset(self):
        return Contrat.objects.filter(agent=self.request.user.agent)
    
class ContratDetailView(DetailView):
    pass

class maintenanceView(ListView):
    model = Maintenance
    template_name = 'home/index.html'
    context_object_name = 'maintenances'
    
    # avoir juste les propriete de proprietaire connecté
    def get_queryset(self):
        return Maintenance.objects.filter(
        propriete__contrat__agent=self.request.user.agent
    ).distinct()
        
class demandeLocationView(ListView):
    model = demandeLocation
    template_name = 'home/index.html'
    context_object_name = 'demandes'
    
    # avoir juste les propriete de proprietaire connecté
    def get_queryset(self):
        return demandeLocation.objects.filter(
        propriete__contrat__agent=self.request.user.agent
    ).distinct()
        
class proprieteListView(ListView):
    model = Propriete
    template_name = 'home/index.html'
    context_object_name = 'proprietes'