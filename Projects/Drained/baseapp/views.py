from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Note
from .forms import NoteForm
from django.db.models import Q


def home(request):
    if not request.user.is_authenticated:
        return render(request, 'baseapp/home_not_login.html')
    else:
        return render(request, 'baseapp/home.html')

def index(request):
    return render(request, 'baseapp/index.html', )


def note_list(request):
    if not request.user.is_authenticated:
        return redirect("Home")
    
    notes = Note.objects.filter(user=request.user)
    return render(request, 'notes/note_list.html', {'notes': notes})


def note_detail(request, pk):
    if not request.user.is_authenticated:
        return redirect("Home")
    
    note = get_object_or_404(Note, pk=pk, user=request.user)
    return render(request, 'notes/note_detail.html', {'note': note})


def add_note(request):
    if not request.user.is_authenticated:
        return redirect("Home")
    
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'notes/add_note.html', {'form': form})


@login_required
def edit_note(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_detail', pk=note.pk)
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/edit_note.html', {'form': form, 'note': note})

def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        note.delete()
        return redirect('note_list')
    return render(request, 'notes/note_detail.html', {'note': note})



@login_required
def search_notes(request):
    query = request.GET.get('q')
    if query:
        notes = Note.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            user=request.user
        )
    else:
        notes = Note.objects.filter(user=request.user)
    
    return render(request, 'notes/search_results_partial.html', {'notes': notes, 'query': query})
