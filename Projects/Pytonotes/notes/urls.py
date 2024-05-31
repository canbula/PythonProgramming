from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create_workspace/', views.create_workspace, name='create_workspace'),
    path('delete_page/<int:page_id>/', views.delete_page, name='delete_page'),
    path('duplicate_page/<int:page_id>/', views.duplicate_page, name='duplicate_page'),
    path('get_page_details/<int:page_id>/', views.get_page_details, name='get_page_details'),
    path('update_page_title/<int:page_id>/', views.update_page_title, name='update_page_title'),
]
