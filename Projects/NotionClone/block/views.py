from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .forms import EditForm, PostForm
from block.models import *
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timedelta
from django.core.serializers.json import DjangoJSONEncoder
from .models import Post, Event, Movie, Birthday
import json
from django.contrib.auth.decorators import login_required
from .models import Post, Birthday, Event, Movie
from .models import Post

# Create your views here.
def homepage(request):
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, "block/homepage.html")


def index(request):
    if not request.user.is_authenticated:
        return redirect('homepage')
    return render(request, "block/index.html")

@login_required
def add_page(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # Veritabanına henüz kaydetme
            post.user = request.user  # Mevcut kullanıcıyı atama
            post.save()  # Veritabanına kaydetme
            messages.success(request, "Post başarıyla oluşturuldu.")
            return redirect('add_page')
        else:
            messages.error(request, "Formda hatalar var. Lütfen tekrar deneyin.")
    else:
        form = PostForm()
    
    return render(request, 'add_page.html', {'form': form, 'posts': Post.objects.all()})

from django.shortcuts import get_object_or_404

def post_detail(request, post_id):
    
    user_id = request.user.id 
    
   
    post = get_object_or_404(Post, pk=post_id, user_id=user_id)
    
    return render(request, 'gorevler.html', {'post': post})





def deleted_posts(request):
    if request.user.is_authenticated:
        deleted_posts = Post.objects.filter(deleted=True, user=request.user)
        return render(request, 'deleted_posts.html', {'deleted_posts': deleted_posts})
    else:
        # Kullanıcı giriş yapmamışsa bir yönlendirme veya uygun bir işlem yapılabilir.
        return HttpResponse("You need to login to view this page.")

def deleted_birthdays(request):
    if request.user.is_authenticated:
        deleted_birthdays = Birthday.objects.filter(deleted=True, user=request.user)
        return render(request, 'deleted_birthdays.html', {'deleted_birthdays': deleted_birthdays})
    else:
        return HttpResponse("You need to login to view this page.")

def deleted_events(request):
    if request.user.is_authenticated:
        deleted_events = Event.objects.filter(deleted=True, user=request.user)
        return render(request, 'deleted_events.html', {'deleted_events': deleted_events})
    else:
        return HttpResponse("You need to login to view this page.")

def deleted_movies(request):
    if request.user.is_authenticated:
        deleted_movies = Movie.objects.filter(deleted=True, user=request.user)
        print(deleted_movies)
        return render(request, 'deleted_movies.html', {'deleted_movies': deleted_movies})
    else:
        return HttpResponse("You need to login to view this page.")


def inbox(request):
    return render(request, 'inbox.html')

def members_settings(request):
    return render(request, 'members_settings.html')




def calendar(request):
   
    user_id = request.user.id  

    events = Event.objects.filter(user_id=user_id, deleted=False)
    birthdays = Birthday.objects.filter(user_id=user_id, deleted=False)

    
    events_data = []
    for event in events:
        events_data.append({
            'title': event.name,
            'start': event.date.isoformat(),  
        })

    
    birthdays_data = []
    for birthday in birthdays:
        birthdays_data.append({
            'title': f"Birthday: {birthday.person_name}",
            'start': birthday.birth_date.isoformat(),  # Tarihi ISO formatına çevir
        })

    data = {
        'events': json.dumps(events_data + birthdays_data),  # Tüm etkinlikleri birleştir
    }
    
    return render(request, 'calendar.html', data)



def templates(request):
    return render(request, 'template.html')

def help_supports(request):
    return render(request, 'help_supports.html')

def trash(request):
    return render(request, 'trash.html')

def birthday(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            person_name = request.POST.get('person_name')
            birth_date = request.POST.get('birth_date')

            birthday = Birthday.objects.create(
                person_name=person_name,
                birth_date=birth_date,
                user=request.user
            )

            birthday.save()
            
            upcoming_birthdays = Birthday.objects.filter(deleted=False, user=request.user).order_by('birth_date')[:6]
            
            return render(request, 'birthday.html', {'upcoming_birthdays': upcoming_birthdays})
        else:
            return HttpResponse("You need to login to view this page.")
    
    upcoming_birthdays = Birthday.objects.filter(deleted=False, user=request.user).order_by('birth_date')[:6]
    return render(request, 'birthday.html',{'upcoming_birthdays': upcoming_birthdays})



def todo(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            product_name = request.POST.get('product_name')
            
            shop = Shopping.objects.create(product_name=product_name, user=request.user)
            shop.save()

            messages.success(request, "Ürün başarıyla eklendi.")

            return redirect('todo')
        else:
            return HttpResponse("You need to login to view this page.")

    shops = Shopping.objects.filter(deleted=False, user=request.user)
    return render(request, 'todo.html', {'shops': shops})

def movie(request):
   
    if request.method == 'POST':
        if request.user.is_authenticated:
            title = request.POST.get('title')
            description = request.POST.get('description')
            movie = Movie.objects.create(
                title=title,
                description=description,
                user=request.user
            )
            
            existing_movie = Movie.objects.filter(title=title, description=description, user=request.user).exists()
            if existing_movie:
                messages.warning(request, "Bu film zaten eklenmiş.")
            else:
                movie.save()
                messages.success(request, "Film başarıyla eklendi.")

            movies=Movie.objects.filter(deleted=False, user=request.user)
            
            return render(request, 'movie.html',{'movies': movies})
    else:
        movies=Movie.objects.filter(deleted=False, user=request.user)
        return render(request, 'movie.html',{'movies': movies})

def shopping(request):
    return render(request, 'shopping.html')
    
def event(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            name = request.POST.get('name')
            date = request.POST.get('date')
            time =request.POST.get('time')

            event = Event.objects.create(
                name=name,
                date=date,
                time=time,
                user=request.user
            )

            event.save()
            
            upcoming_events = Event.objects.filter(deleted=False, user=request.user).order_by('date')[:3]

            
            return render(request, 'event.html', {'upcoming_events': upcoming_events})
    upcoming_events = Event.objects.filter(deleted=False, user=request.user).order_by('date')[:3]
    return render(request, 'event.html', {'upcoming_events': upcoming_events})



def delete_post(request, post_id):
    # Post nesnesini al veya 404 hatası gönder
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        # Post nesnesinin deleted alanını True olarak işaretle
        post.deleted = True
        post.save()
        
        
        # Eğer başka bir sayfaya yönlendirme yapmak istiyorsanız, burada onu belirtin
        return redirect('add_page')
    
    # Eğer gönderim yöntemi "GET" ise, sadece sayfayı göster
    return render(request, 'add_page.html')
def delete_birthday(request, birthday_id):
   
    delete_birthday = get_object_or_404(Birthday, id=birthday_id)
    
    if request.method == 'POST':
        delete_birthday.deleted = True
        delete_birthday.save()
        return redirect('birthday')
    return render(request, 'birthday.html')


def delete_event(request, event_id):
    delete_event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        delete_event.deleted = True
        delete_event.save()
        return redirect('event')
    return render(request, 'event.html')


def delete_movie(request, movie_id):   
    delete_movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'POST':
        delete_movie.deleted = True
        delete_movie.save()
        return redirect('movie')
    
    return render(request, 'movie.html')



def edit_post(request, post_id):
    # Post nesnesini getir veya 404 hatası göster
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        # Formdan gelen verileri al
        form = EditForm(request.POST)
        if form.is_valid():
            # Form doğru ise, gönderiyi güncelle
            post.title = form.cleaned_data['title']
            post.body = form.cleaned_data['body']
            post.save()
            # Başka bir sayfaya yönlendir veya mesaj göster
            return redirect('post_detail', post_id=post.id)
    else:
        #
        form =EditForm(initial={'title': post.title, 'body': post.body}) 
        return render(request, 'edit_post.html', {'form': form})

    
    
def undo_delete_post(request, post_id):
    # Post nesnesini al veya 404 hatası gönder
    post = get_object_or_404(Post, id=post_id)

   
    post.deleted = False
    post.save()

    # İlgili sayfaya yönlendir
    return redirect('deleted_posts')

def undo_delete_movies(request,movie_id):
    # Post nesnesini al veya 404 hatası gönder
    movie = get_object_or_404(Movie, id=movie_id)

    # Post nesnesinin deleted alanını False olarak işaretle
    movie.deleted = False
    movie.save()

    # İlgili sayfaya yönlendir
    return redirect('deleted_movies')


def undo_delete_events(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Post nesnesinin deleted alanını False olarak işaretle
    event.deleted = False
    event.save()

    # İlgili sayfaya yönlendir
    return redirect('deleted_events')


def undo_delete_birthdays(request, birthday_id):
    # Post nesnesini al veya 404 hatası gönder
    birthday = get_object_or_404(Birthday, id=birthday_id)

    # Post nesnesinin deleted alanını False olarak işaretle
    birthday.deleted = False
    birthday.save()

    # İlgili sayfaya yönlendir
    return redirect('deleted_birthdays')

def edit_shop(request, shop_id):
    # Düzenlenmek istenen alışveriş öğesini getir
    shop = get_object_or_404(Shopping, id=shop_id)
    
    if request.method == 'POST':
        # POST isteği işleniyor
        # Formdan gelen verileri al
        product_name = request.POST.get('product_name')
        
        # Alışveriş öğesini güncelle
        shop.product_name = product_name
        shop.save()

        # Başarılı bir mesaj gönder
        messages.success(request, "Ürün başarıyla güncellendi.")

        # Alışveriş listesine yönlendir
        return redirect('todo')

    # GET isteği durumunda, düzenleme formunu göster
    return render(request, 'edit_shop.html', {'shop': shop})


def delete_shop(request, shop_id):
    shop = get_object_or_404(Shopping, id=shop_id)
    print(shop)
    if request.method == 'POST':
        shop.deleted = True
        shop.save()
        return redirect('todo')

    return render(request, 'todo.html', {'shop': shop})
