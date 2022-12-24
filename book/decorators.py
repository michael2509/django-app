from .models import Library
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

# decorator to check if a user is authenticated and has role bookseller and is owner of the library
def owner_required(function):
    def wrap(request, *args, **kwargs):
        library = get_object_or_404(Library, id=kwargs['library_id'])
        if not request.user.is_authenticated:
            messages.error(request, 'Veuillez vous connecter pour accéder à cette page')
            return redirect('/accounts/login/')
        if request.user.role != 'bookseller':
            messages.error(request, 'Vous n\'avez pas le role nécéssaire pour accéder à cette page')
            return redirect('/accounts/login/')
        if request.user not in library.owners.all():
            messages.error(request, 'Vous n\'êtes pas propriétaire de cette bibliothèque')
            return redirect('/accounts/login/')
        else:
            return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

# decorator to check if a user is authenticated and has role bookseller
def bookseller_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Veuillez vous connecter pour accéder à cette page')
            return redirect('/accounts/login/')
        if request.user.role != 'bookseller':
            messages.error(request, 'Vous n\'avez pas le role nécéssaire pour accéder à cette page')
            return redirect('/accounts/login/')
        else:
            return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap