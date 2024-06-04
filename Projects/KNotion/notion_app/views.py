from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
# burda urls içinde kullanılabilmesi için fonksiyonlar yazacağız.
def index (request):
    return render(request, "notion_app/index.html")
def add_page (request):
    return render(request, "notion_app/add_page.html")
def calender (request):
    return render(request, "notion_app/calender.html")
def help (request):
    return render(request, "notion_app/help.html")
def inbox (request):
    return render(request, "notion_app/inbox.html")
def template (request):
    return render(request, "notion_app/template.html")
def trash (request):
    return render(request, "notion_app/trash.html")
def settingsmember (request):
    return render(request, "notion_app/settingsmember.html")
def base (request):
    return render(request, "notion_app/base.html")
def reading_list (request):
    return render(request, "notion_app/reading_list.html")
def meal_list (request):
    return render(request, "notion_app/meal_list.html")
def todolist (request):
    return render(request, "notion_app/todolist.html")
def quick_note (request):
    return render(request, "notion_app/quick_note.html")












