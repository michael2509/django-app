from django.forms import ModelForm, DateInput as BaseDateInput
from .models import Book, BookInstance

class DateInput(BaseDateInput):
    input_type = 'date'

class AddBookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'editor', 'genre', 'cover']


class BorrowBookForm(ModelForm):
    class Meta:
        model = BookInstance
        fields = ['borrower', 'borrow_date', 'return_date']
        widgets = {
            'borrow_date': DateInput(),
            'return_date': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['borrow_date'].required = True
        # self.fields['return_date'].required = True