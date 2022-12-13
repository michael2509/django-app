from django.contrib import admin
from .models import Book, Book_instance, Library

# Register your models here.
admin.site.register(Book)
admin.site.register(Book_instance)
admin.site.register(Library)
