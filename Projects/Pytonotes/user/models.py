from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

def get_profile_image_path(self, filename):
    return f"profiles/{self.pk}/profile_image.png"

def default_profile_image():
    return "images/default_user.png"

class CustomAccountManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError("You must have an email address.")
        if not name:
            raise ValueError("You must have a name.")
        user = self.model(
            email=self.normalize_email(email),
            name=name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, name, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    objects = CustomAccountManager()
    
    email = models.EmailField(
        verbose_name="Email", 
        max_length=100, 
        unique=True
    )
    name = models.CharField(
        verbose_name="Name",
        max_length=50,
        default="name",
        unique=False
    )
    date_joined = models.DateTimeField(
        verbose_name="Date Joined", 
        auto_now_add=True
    )
    last_login = models.DateTimeField(
        verbose_name="Last Login",
        auto_now=True
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(
        max_length=255,
        upload_to=get_profile_image_path,
        null=True,
        blank=True,
        default=default_profile_image
    )
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]
    
    def __str__(self):
        return self.name
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
