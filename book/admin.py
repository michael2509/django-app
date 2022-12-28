from django.contrib import admin
from .models import Book, BookInstance, Library, LectureGroup, Message

# Register your models here.
admin.site.register(Book)
admin.site.register(BookInstance)
admin.site.register(Library)
admin.site.register(LectureGroup)
admin.site.register(Message)