from django.forms import ModelForm, HiddenInput
from .models import BookInstance, Library

class AddBookForm(ModelForm):
    class Meta:
        model = BookInstance
        fields = ['book', 'library']
        widgets = {'library': HiddenInput()}


class BorrowBookForm(ModelForm):
    class Meta:
        model = BookInstance
        fields = ['borrower']