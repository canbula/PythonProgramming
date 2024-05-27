from django.shortcuts import  redirect, render
from django.contrib.auth import logout


def main(request):
    return render(request, "index.html")

def user_logout(request):
    logout(request)
    return redirect('/')