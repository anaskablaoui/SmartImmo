from django.shortcuts import render,redirect
from .forms import RegisterForm,LoginForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Proprietaire
from django.contrib import messages

# Create your views here.

def auth_view(request):
    login_form = LoginForm()
    register_form = RegisterForm()
    error = None

    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "login":
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                email    = login_form.cleaned_data["email"]
                password = login_form.cleaned_data["password"]
                user = authenticate(request, username=email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("home")
                else:
                    error = "Email ou mot de passe incorrect"

        elif form_type == "register":
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                nom      = register_form.cleaned_data.get("nom")
                prenom   = register_form.cleaned_data.get("prenom")
                email    = register_form.cleaned_data.get("email")
                password = register_form.cleaned_data.get("password")
                proprietaire = Proprietaire.objects.create_user(
                    nom=nom, prenom=prenom, email=email, password=password
                )
                login(request, proprietaire)
                return redirect("home")
            else:
                error = "Veuillez corriger les erreurs."

    return render(request, "accounts/index.html", {
        "loginForm": login_form,
        "registerForm": register_form,
        "error": error,
    })



@login_required
def homeView(request):
    pass