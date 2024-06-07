from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render
from pyexpat.errors import messages

from .database import Database, auth
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm


database =Database()

def home(request):
    data=database.get_data()
    return render(request,"noteisapp/home.html",{'data':data})


def todo_list(request):
    return render(request,"noteisapp/todo_list.html")

def calendar(request):
    return render(request,"noteisapp/calendar.html")

def quick_notes(request):
    return render(request,"noteisapp/quick_notes.html")

def reading_list(request):
    return render(request,"noteisapp/reading_list.html")

def login_page_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = auth.sign_in_with_email_and_password(email, password)

            if user:
                request.session['uid'] = user['localId']
                return render(request, 'noteisapp/home.html')
            else:
                error_message = "Invalid email or password. Please try again."
                return render(request, 'noteisapp/login.html', {'error_message': error_message})

        except Exception as e:
            error_message = " Invalid password or email! "
            return render(request, 'noteisapp/login.html', {'error_message': error_message})
    else:
        return render(request, 'noteisapp/login.html')

def register_page_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if len(password) < 6 or not any(char.isupper() for char in password):
            error_message = "The password must be at least 6 characters long and must contain at least one uppercase letter."
            return render(request, 'noteisapp/register.html', {'error_message': error_message})

        try:
            database.register(email, password)
            return render(request, 'noteisapp/home.html')
        except Exception as e:
            error_message = "Email address already exist!"
            return render(request, 'noteisapp/register.html', {'error_message': error_message})
    else:
        return render(request, 'noteisapp/register.html')
    


def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = auth.sign_in_with_email_and_password(email, password)

            if user:
                request.session['uid'] = user['localId']
                return render(request, 'noteisapp/home.html')
            else:
                error_message = "Invalid email or password. Please try again."
                return render(request, 'login.html', {'error_message': error_message})

        except Exception as e:
            error_message = "An error occurred: {}".format(str(e))
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')



def register_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            database.register(email, password)
            return render(request, 'noteisapp/home.html')
        except Exception as e:
            error_message = "An error occurred: {}".format(str(e))
            return render(request, 'register.html', {'error_message': error_message})
    else:
        return render(request, 'register.html')




def quick_notes(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        database.adddata(title,content)
    return render(request,'noteisapp/quick_notes.html')


def delete_note(request, key):
    if request.method == 'POST':
        database.delete_data(key)
    return redirect('home')