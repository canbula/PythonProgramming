from django.urls import path
from . import views 
from .views import *


urlpatterns = [
   
    path('', views.homepage, name='homepage'),
    path("index/",views.index ,name="index"),
    path('add_page/', views.add_page, name='add_page'),
    path('deleted_posts/', views.deleted_posts, name='deleted_posts'),
    path('deleted_birthdays/', views.deleted_birthdays, name='deleted_birthdays'),
    path('deleted_events/', views.deleted_events, name='deleted_events'),
    path('deleted_movies/', views.deleted_movies, name='deleted_movies'),
    path('post/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('event/delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('movie/delete/<int:movie_id>/', views.delete_movie, name='delete_movie'),
    path('birthday/delete/<int:birthday_id>/', views.delete_birthday, name='delete_birthday'),
    path('post/edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('inbox/', views.inbox, name='inbox'),
    path('members_settings/', views.members_settings, name='members_settings'),
    path('calendar/', views.calendar, name='calendar'),
    path('templates/', views.templates, name='templates'),
    path('help_supports/', views.help_supports, name='help_supports'),
    path('trash/', views.trash, name='trash'),
    path('birthday/', views.birthday, name='birthday'),
    path('todo/', views.todo, name='todo'),
    path('movie/', views.movie, name='movie'),
    path('event/', views.event, name='event'),
    path('shopping/', views.shopping, name='shopping'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('undo_delete_post/<int:post_id>/', views.undo_delete_post, name='undo_delete_post'),
    path('undo_delete_birthdays/<int:birthday_id>/', views.undo_delete_birthdays, name='undo_delete_birthdays'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('undo_delete_events/<int:event_id>/', views.undo_delete_events, name='undo_delete_event'),
    path('undo_delete_movies/<int:movie_id>/', views.undo_delete_movies, name='undo_delete_movie'),
    path('edit/<int:shop_id>/', views.edit_shop, name='edit_shop'),
    path('delete/<int:shop_id>/', views.delete_shop, name='delete_shop'),
    
]

