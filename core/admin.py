from django.contrib import admin
from .models import Author, Category, Book

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'created_at', 'updated_at']
    list_display_links = ['last_name', 'first_name']
    ordering = ['last_name']
    search_fields = ['last_name', 'first_name']
    list_per_page = 10

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    ordering = ['name']
    search_fields = ['name']

class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'author', 'pub_date', 'created_at', 'updated_at']
    ordering = ['title']
    search_fields = ['title', 'category__name', 'author__last_name', 'author__first_name']
    list_per_page = 10
     
admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Book, BookAdmin)
