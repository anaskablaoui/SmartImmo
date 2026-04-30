
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import loginForm
from .models import Agents
from django.contrib import messages

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
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password.')
        return render(request, 'login/index.html', {'form': form})


@login_required
def homeView(request):
    return redirect('home/home.html')
    
