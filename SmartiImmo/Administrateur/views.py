from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views import View
from .forms import adminLoginForm
from django.contrib import messages
from django.views.generic import ListView,DetailView
from .forms import AjoutAgentForm
from Agents.models import Agents,Baux
from Proprietaire.models import Propriete


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
    
    agents     = Agents.objects.all()      # ← tous les agents
    proprietes = Propriete.objects.all()   # ← toutes les proprietes
    baux       = Baux.objects.all()        # ← tous les baux

    return render(request, 'adminDashboard/index.html', {
        'form'      : form,
        'agents'    : agents,
        'proprietes': proprietes,
        'baux'      : baux,
    })
    
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
