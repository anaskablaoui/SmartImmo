from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views import View
from .forms import adminLoginForm
from django.contrib import messages
from django.views.generic import ListView,DetailView
from .forms import AjoutAgentForm
from Agents.models import Agents,Baux
from Proprietaire.models import Propriete
from .models import Administrateur


from django.db.models import Sum
from django.db.models.functions import TruncMonth
# Create your views here.

class LoginView(View):
    def get(self,request):
        form=adminLoginForm()
        return render(request,'adminLogin/index.html',{'form':form})
    
    def post(self,request):
        form=adminLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request,email=email,password=password)
            if user is not None:
                login(request,user)
                return redirect('adminDashboard')
            else:
                messages.error(request,'Invalid email or password.')
        return render(request,'adminLogin/index.html',{'form':form})

def logoutView(request):
    if request.method =='POST':
        logout(request)
        return redirect('adminLogin')
    return redirect('adminDashboard')

@login_required(login_url='/administrateur/')
def homeView(request):
    if request.method == 'POST':
        form = AjoutAgentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminDashboard')
    else:
        form = AjoutAgentForm()
    
    baux_par_mois = (
    Baux.objects
    .annotate(mois=TruncMonth('date_debut'))
    .values('mois')
    .annotate(total_prix=Sum('prix'))
    .order_by('mois')
    )
    
    labels = [n['mois'].strftime('%B %Y') for n in baux_par_mois]
    data= [float(n['total_prix'])*0.3 for n in baux_par_mois]
    agents     = Agents.objects.all()      # ← tous les agents
    proprietes = Propriete.objects.all()   # ← toutes les proprietes
    baux       = Baux.objects.all()        # ← tous les baux

    return render(request, 'adminDashboard/index.html', {
        'form'      : form,
        'agents'    : agents,
        'proprietes': proprietes,
        'baux'      : baux,
        'chart_labels': labels,
        'chart_data': data,
        'admin':request.user
    })
    
    
def supprimerAgent(request, agent_id):
    
    agent = get_object_or_404(Agents, id=agent_id)
    agent.delete()        
    return redirect('adminDashboard')
    
    
    
class agentListView(ListView):
    model = Agents
    template_name = 'adminDashboard/index.html'
    context_object_name = 'agents'
     
class agentDetailView(DetailView):
    model = Agents
    template_name = 'adminDashboard/index.html'
    context_object_name = 'agent'

class proprieteListView(ListView):
    model = Propriete
    template_name = 'adminDashboard/index.html'
    context_object_name = 'proprietes'

class bauxListView(ListView):
    model = Baux
    template_name = 'adminDashboard/index.html'
    context_object_name = 'baux'

class bauxDetailView(DetailView):
    model = Baux
    template_name = 'adminDashboard/index.html'
    context_object_name = 'baux'
