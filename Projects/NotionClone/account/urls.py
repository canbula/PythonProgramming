from django.urls import path
from . import views
from .views import change_password


urlpatterns = [
        path('login/', views.user_login, name='user_login'),
        path("register/",views.user_register ,name="user_register"),
        path("logout/",views.user_logout ,name="user_logout"),
        path('change-password/', views.change_password, name='change_password'),
     
    ]

