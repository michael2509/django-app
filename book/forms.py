from django.forms import ModelForm
from .models import Book, BookInstance

class AddBookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'editor', 'genre', 'cover']


class BorrowBookForm(ModelForm):
    class Meta:
        model = BookInstance
        fields = ['borrower']
