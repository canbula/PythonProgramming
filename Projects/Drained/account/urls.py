from django.urls import path
from . import views

urlpatterns = [
    path("login", views.login_request, name="login"),
    path("singup", views.singup_request, name="singup"),
    path("logout", views.logout_request, name="logout"),
    
]
