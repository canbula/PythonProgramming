from . import views
from django.urls import path


urlpatterns = [
    path('home/', views.home,name='home'),
    path('', views.login_page_view, name='login'),
    path('register/', views.register_page_view, name='register'),
    path('todo_list/', views.todo_list, name='todo_list'),
    path('quick_notes/', views.quick_notes, name='quick_notes'),
    path('calendar/', views.calendar, name='calendar'),
    path('reading_list/', views.reading_list, name='reading_list'),
    path('delete/<str:key>/', views.delete_note, name='delete_note'),
  
    
]
