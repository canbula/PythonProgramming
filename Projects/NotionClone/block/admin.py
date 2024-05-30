from django.contrib import admin
from .models import Post, Event, Movie, Shopping, Birthday

class PostAdmin(admin.ModelAdmin):
    list_display = ('title',)
    actions = ['delete_selected']  # Ekle

    def delete_selected(self, request, queryset):  # Ekle
        queryset.delete()
    delete_selected.short_description = "Delete selected posts"

class EventAdmin(admin.ModelAdmin):
    list_display = ('name',)
    actions = ['delete_selected']

    def delete_selected(self, request, queryset):
        queryset.delete()
    delete_selected.short_description = "Delete selected events"

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title',)
    actions = ['delete_selected']

    def delete_selected(self, request, queryset):
        queryset.delete()
    delete_selected.short_description = "Delete selected movies"

class ShoppingAdmin(admin.ModelAdmin):
    list_display = ('product_name',)
    actions = ['delete_selected']

    def delete_selected(self, request, queryset):
        queryset.delete()
    delete_selected.short_description = "Delete selected shoppings"

class BirthdayAdmin(admin.ModelAdmin):
    list_display = ('person_name',)
    actions = ['delete_selected']

    def delete_selected(self, request, queryset):
        queryset.delete()
    delete_selected.short_description = "Delete selected birthdays"


admin.site.register(Post, PostAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Shopping, ShoppingAdmin)
admin.site.register(Birthday, BirthdayAdmin)
