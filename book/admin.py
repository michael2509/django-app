from django.contrib import admin
from .models import Book, BookInstance, Library

# Register your models here.
admin.site.register(Book)
admin.site.register(BookInstance)
admin.site.register(Library)
