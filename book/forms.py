from django.forms import ModelForm
from .models import BookInstance

class AddBookForm(ModelForm):
    class Meta:
        model = BookInstance
        fields = ['book', 'library']