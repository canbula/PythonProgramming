from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
class AdminUser(UserAdmin):
    list_display        = ("email", "name", "date_joined", "last_login", "is_admin", "is_staff")
    search_fields       = ("email", "name")
    readonlu_fields     = ("id", "date_joined", "last_login")
    
    filter_horizontal   = ()
    list_filter         = ()
    fieldsets           = ()
    ordering            = ('email',)
        
admin.site.register(CustomUser, AdminUser)