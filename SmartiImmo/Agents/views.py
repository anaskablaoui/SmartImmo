
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import loginForm
from .models import Agents,Baux
from django.contrib import messages
from django.views.generic import ListView,DetailView

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
def homeView(request):
    return render(request,'home/home.html')
    
class BauxListView(ListView):
    model = Baux
    template_name = 'home/index.html'
    context_object_name = 'Baux'
    
    # avoir juste les propriete de proprietaire connecté
    def get_queryset(self):
        return Baux.objects.filter(agent=self.request.user.agent)