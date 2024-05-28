from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from .models import CustomUser
from .forms import SignupForm, LoginPhaseOneForm, LoginPhaseTwoForm

def user_login(request):
    user = request.user
    if user.is_authenticated:
        return HttpResponseRedirect("/")
    email = request.POST.get("email")
    if not email or email == "":
        form = LoginPhaseOneForm(request.POST)
        return render(request, 
                      "authentication/login.html", 
                      { "form": form, "phaseOne": True, "title": "Login" }
        )
    else:
        if CustomUser.objects.filter(email=email).exists():
            form = LoginPhaseTwoForm(request.POST)
            if form.is_valid():
                password = request.POST['password']
                account = authenticate(email=email, password=password)
                if account:
                    login(request,account)
                    return redirect('/')
            return render(request, "authentication/login.html", { "form": form, "title": "Login"})
        else:
            form = SignupForm(request.POST)
            return render(request, "authentication/register.html", { "form": form, "title": "Register"})
    

def user_register(request):
    user = request.user
    if user.is_authenticated:
        return HttpResponseRedirect("/")
    form = SignupForm(request.POST)
    if form.is_valid():
        form.save()
        email = form.cleaned_data.get('email').lower()
        password1 = form.cleaned_data.get('password1')
        account = authenticate(email=email,password=password1)
        login(request,account)
        return redirect("/")
    return render(request, "authentication/register.html", { "form": form, "title": "Register" }) 

     
def user_logout(request):
    logout(request)
    return redirect('/')