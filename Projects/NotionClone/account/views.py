from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from account.forms import  LoginUserForm ,RegisterUserForm
from django.contrib import messages
from django.views.generic.edit import FormView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash




@csrf_exempt
def user_login(request):
    if request.method == "POST":
        form = LoginUserForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_active:
                login(request, user)
                return redirect('add_page')
            else:
                return render(request, 'account/login.html', {'form': form})
        else:
            return render(request, 'account/login.html', {'form': form})

    form = LoginUserForm()
    return render(request, 'account/login.html', {'form': form})
               

@csrf_exempt
def user_register(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user_login")
        else:
            return render(request, "account/register.html",{"form":form})
    
    form = RegisterUserForm()
    return render(request, "account/register.html", {"form": form})


    
def user_logout(request):
    logout(request)
    return redirect('homepage')

from django.contrib import messages

@csrf_exempt
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            print("1")
            user = form.save()
            update_session_auth_hash(request, user)  # Oturum açıkken oturumun geçerliliğini koru
            messages.success(request, 'Your password was successfully updated!')
            return redirect('members_settings')  # Şifre değiştikten sonra profil sayfasına yönlendir
        else:
            # Form geçerli değilse, hata mesajlarını alıp kullanıcıya göster
            print("2")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        print("1")
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'members_settings.html', {'form': form})








