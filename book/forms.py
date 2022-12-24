from django.forms import ModelForm
from .models import BookInstance, Library

class AddBookForm(ModelForm):
    class Meta:
        model = BookInstance
        fields = ['book', 'library']

    # select only libraries that the user is owner of
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(AddBookForm, self).__init__(*args, **kwargs)
        self.fields['library'].queryset = Library.objects.filter(owners=user)


class BorrowBookForm(ModelForm):
    class Meta:
        model = BookInstance
        fields = ['borrower']