from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import CustomUser

class SignupForm(UserCreationForm):
    password2 = None
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({
            "name": "name",
            "id": "name",
            "type": "text",
            "class": "form-control",
            "placeholder":"Bill Gates, Bill, BG"
        })
        self.fields["password1"].widget.attrs.update({
            "name": "password1",
            "id": "password1",
            "type": "password",
            "class": "form-control",
            "placeholder":"Password"
        })   
    
    class Meta:
        model = CustomUser
        fields = ["email", "name", "password1"]
        
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = CustomUser.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"Email {email} is already in use!")
        


class LoginPhaseOneForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({
            "name": "email",
            "id": "email",
            "type": "email",
            "class": "form-control",
            "placeholder":"Enter your email address..."
        })        
        
    
    class Meta:
        model = CustomUser
        fields = ["email"]
        
        

class LoginPhaseTwoForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({
            "name": "email",
            "id": "email",
            "type": "text",
            "class": "form-control",
            "placeholder":"Bill Gates, Bill, BG"
        })
        self.fields["password"].widget.attrs.update({
            "name": "password",
            "id": "password",
            "class": "form-control",
            "placeholder":"Password"
        })   
    
    class Meta:
        model = CustomUser
        fields = ["email", "password"]
        
    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid Account!")