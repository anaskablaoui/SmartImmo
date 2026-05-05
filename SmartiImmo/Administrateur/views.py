from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import View
from .forms import adminLoginForm
from django.contrib import messages

from Agent.models import Agents, Baux
from Proprietaire.models import Proprietaire, Propriete
from Locataire.models import Locataire

class LoginView(View):
    def get(self, request):
        form = adminLoginForm()
        return render(request, 'adminLogin/index.html', {'form': form})

    def post(self, request):
        form = adminLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('adminDashboard')
            else:
                messages.error(request, 'Invalid email or password.')
        return render(request, 'adminLogin/index.html', {'form': form})


def logoutView(request):
    if request.method == 'POST':
        logout(request)
        return redirect('adminLogin')
    return redirect('adminDashboard')


@login_required(login_url='/administrateur/')
def homeView(request):
    context = {
        'agents_list':      Agents.objects.select_related('user').all(),
        'baux_list':        Baux.objects.select_related('locataire__user', 'propriete', 'agent__user', 'proprietaire__user').all(),
        'proprietes_list':  Propriete.objects.select_related('proprietaire__user').all(),
        'locataires_list':  Locataire.objects.select_related('user').all(),
        # Stats
        'total_agents':     Agents.objects.count(),
        'total_baux':       Baux.objects.count(),
        'total_proprietes': Propriete.objects.count(),
        'total_locataires': Locataire.objects.count(),
    }
    return render(request, 'adminDashboard/index.html', context)

