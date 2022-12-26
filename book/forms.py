from django.forms import ModelForm, DateInput as BaseDateInput, DateTimeInput as BaseDateTimeInput, HiddenInput
from .models import Book, BookInstance, LectureGroup

class DateInput(BaseDateInput):
    input_type = 'date'

class DateTimeInput(BaseDateTimeInput):
    input_type = 'datetime-local'

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


class CreateLectureGroupForm(ModelForm):
    class Meta:
        model = LectureGroup
        fields = ['library', 'participants', 'startDateTime', 'endDateTime']
        widgets = {
            'library': HiddenInput(),
            'startDateTime': DateTimeInput(),
            'endDateTime': DateTimeInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['library'].required = True
        self.fields['participants'].required = True
        self.fields['startDateTime'].required = True
        self.fields['endDateTime'].required = True