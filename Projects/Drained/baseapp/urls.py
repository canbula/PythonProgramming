from django.urls import path
from . import views
from .views import note_list, add_note, note_detail, home, edit_note, delete_note


urlpatterns = [
    path("", home , name="Home"),
    path("index",views.index),
    path('notes/', note_list, name='note_list'),
    path('notes/add/', add_note, name='add_note'),
    path('notes/<int:pk>/', note_detail, name='note_detail'),
    path('notes/<int:pk>/edit/', edit_note, name='edit_note'),
    path('note/<int:pk>/delete/', delete_note, name='delete_note'),
    path('notes/search/', views.search_notes, name='search_notes'),  # Add this line
    ]