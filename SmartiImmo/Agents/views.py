from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import loginForm,accepterlocationForm
from .models import Agents,Baux,Contrat
from django.contrib import messages
from django.views.generic import ListView,DetailView
from Locataire.models import Maintenance
from Proprietaire.models import Propriete
from Locataire.models import demandeLocation
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
def homeView(request,offre_id=None):

    if request.method == 'POST':
        demande = get_object_or_404(demandeLocation, id=offre_id)
        form=accepterlocationForm(request.POST)
        if form.is_valid():
            Baux.objects.create(
            locataire=demande.locataire,
            agent=request.user.agent,
            propriete=demande.propriete,
            proprietaire=demande.propriete.proprietaire,
            prix=demande.prix,
            date_debut=demande.date_entre,
            date_sortie=demande.date_sortie
        )
            demande=demandeLocation.objects.get(id=offre_id)
            demande.delete()
            
            messages.success(request, 'Location acceptée avec succès.')
            return redirect('agentDashboard')

    return render(request,'home/home.html',{
        'demandes':demandeLocation.objects.all(),
        'maintenances':Maintenance.objects.filter(propriete__contrat__agent=request.user.agent).distinct(),
        'contrats':Contrat.objects.filter(agent=request.user.agent),
        'Baux':Baux.objects.filter(agent=request.user.agent),
        
        })
    
def imprimer_baux(request, bail_id):
    bail = get_object_or_404(Baux, id=bail_id)
    return render(request, 'home/baux.html', {
        'bail': bail
    })

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