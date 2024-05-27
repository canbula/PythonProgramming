from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include("user.urls")),
    path('user/', include("django.contrib.auth.urls")),
    path('notes/', include('notes.urls')), 
    path('logout/', views.user_logout, name="logout"),
    path('', RedirectView.as_view(url='/notes/', permanent=False)),  # Redirect root URL to /notes/
]
