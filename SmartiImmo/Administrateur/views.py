from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views import View
from .forms import adminLoginForm
from django.contrib import messages
# Create your views here.

class LoginView(View):
    def get(self,request):
        form=adminLoginForm()
        return render(request,'adminLogin/index.html',{'form':form})
    
    def post(self,request):
        form=adminLoginForm(request.POST)
        if form.is_valid():
            matricule=form.cleaned_data['matricule']
            password = form.cleaned_data['password']
            user = authenticate(request,matricule=matricule,password=password)
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

@login_required
def homeView(request):
    return render(request,'adminDashboard/index.html')

