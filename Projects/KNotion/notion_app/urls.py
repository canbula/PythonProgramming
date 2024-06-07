from django.urls import path
from.import views


urlpatterns = [
   #ilk olarak index sayfasına gideceğiz.
    path('',views.index , name="index"),
    path('add_page/',views.add_page , name="add_page"),
    path('calender/',views.calender , name="calender"),
    path('help/',views.help , name="help"),
    path('inbox/',views.inbox , name="inbox"),
    path('template/',views.template , name="template"),
    path('trash/',views.trash , name="trash"),
    path('settingsmember/',views.settingsmember , name="settingsmember"),
    path('base/',views.base , name="base"),
    path('reading_list/',views.reading_list , name="reading_list"),
   


    path('meal_list/',views.meal_list , name="meal_list"),
    path('todolist/',views.todolist , name="todolist"),
    path('quick_note/',views.quick_note , name="quick_note"),
    
]
