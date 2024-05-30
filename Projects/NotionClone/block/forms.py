from django import forms
from .models import Post
from ckeditor.widgets import CKEditorWidget
from django.forms import formset_factory

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body']
        widgets = {
            'body': CKEditorWidget()
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Untitled', 'style': 'color: black; border:none;'}),
        }

class EditForm(forms.Form):
    title = forms.CharField(
        label='Title',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    body = forms.CharField(
        label='Bodefrjky',
        widget=CKEditorWidget()
    )
   
    