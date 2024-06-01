from django.contrib import admin
from .models import Note
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at')
    search_fields = ('title', 'content', 'user__username')
    list_filter = ('created_at', 'updated_at', 'user')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

admin.site.register(Note, NoteAdmin)

# If you need to customize the User model admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
