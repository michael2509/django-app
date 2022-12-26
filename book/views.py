from django.shortcuts import get_object_or_404, render
from .models import Library, BookInstance
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import AddBookForm, BorrowBookForm
from .decorators import owner_required, bookseller_required
from datetime import date


def home(request):
    return render(request, 'book/index.html')

def libraries(request):
    if 'department_code' in request.GET:
        department_code = request.GET.get('department_code')
        libraries = Library.objects.filter(department_code=department_code)
        return render(request, 'library/index.html', {'libraries': libraries})

    else:
        libraries = Library.objects.all()
        return render(request, 'library/index.html', {'libraries': libraries})


def search(request):
    if 'book_name' in request.GET:
        book_name = request.GET.get('book_name')
        book_instances = BookInstance.objects.filter(book__title__icontains=book_name)

        # create a list of dict with a key title that contains the title of the book without duplicates
        # and a key libraries that contains a list of libraries that have this book without duplicates
        books_infos = []
        for book_instance in book_instances:
            if len(books_infos) == 0 or book_instance.book.title != books_infos[-1]['book'].title:
                books_infos.append({'book': book_instance.book, 'libraries': []})
            if len(books_infos[-1]['libraries']) == 0 or book_instance.library != books_infos[-1]['libraries'][-1]:
                books_infos[-1]['libraries'].append(book_instance.library)

        return render(request, 'book/search.html', {'books_infos': books_infos})
    else:
        return render(request, 'book/search.html')


@owner_required
def add_book(request, library_id):

    if request.method == 'GET':
        book_form = AddBookForm()

        return render(request, 'book/add_book.html', {'library_id': library_id, 'book_form': book_form})

    if request.method == 'POST':
        book_form = AddBookForm(request.POST, request.FILES)

        if book_form.is_valid():
            book = book_form.save()
            BookInstance.objects.create(book=book, library_id=library_id)
            messages.success(request, 'Book added successfully')            
            return redirect('library', library_id=library_id)
        else:
            messages.error(request, 'Error adding book')
            return render(request, 'book/add_book.html', {'book_form': book_form, 'library_id': library_id})


@bookseller_required
def libraries_owned(request):
    libraries = Library.objects.filter(owners=request.user)
    return render(request, 'library/libraries_owned.html', {'libraries': libraries})
    

@owner_required
def library(request, library_id):

    library = get_object_or_404(Library, id=library_id)

    if request.GET.get('book_name') and not request.GET.get('borrower_name'):
        book_name = request.GET.get('book_name')
        book_instances = BookInstance.objects.filter(book__title__icontains=book_name, library=library)

    if request.GET.get('borrower_name') and not request.GET.get('book_name'):
        borrower_name = request.GET.get('borrower_name')
        book_instances = BookInstance.objects.filter(borrower__username__icontains=borrower_name, library=library)


    if request.GET.get('book_name') and request.GET.get('borrower_name'):
        book_name = request.GET.get('book_name')
        borrower_name = request.GET.get('borrower_name')
        book_instances = BookInstance.objects.filter(book__title__icontains=book_name, borrower__username__icontains=borrower_name, library=library)

    if not request.GET.get('book_name') and not request.GET.get('borrower_name'):
        book_instances = BookInstance.objects.filter(library=library)
    
    return render(request, 'library/library.html', {'library': library, 'book_instances': book_instances})

@owner_required
def borrow_book(request, library_id):
    if request.method == 'GET':
        book_instance_id = request.GET.get('book_instance_id')
        book_instance = get_object_or_404(BookInstance, id=book_instance_id)
        borrow_form = BorrowBookForm(initial={
            'book_instance': book_instance,
            'borrower': book_instance.borrower,
            'borrow_date': book_instance.borrow_date,
            'return_date': book_instance.return_date
        })
        return render(request, 'book/borrow_book.html', {'library_id': library_id, 'book_instance': book_instance, 'borrow_form': borrow_form})

    if request.method == 'POST':
        book_instance_id = request.POST.get('book_instance_id')
        book_instance = get_object_or_404(BookInstance, id=book_instance_id)
        borrow_form = BorrowBookForm(request.POST, instance=book_instance)

        if borrow_form.is_valid():
            borrow_form.save()
            messages.success(request, 'Emprunt mis à jour')
        else:
            print(borrow_form.errors)
            messages.error(request, 'Erreur durant l\'emprunt')

    return redirect('library', library_id=library_id)

@owner_required
def late_borrow_list(request, library_id):
    library = get_object_or_404(Library, id=library_id)
    book_instances = BookInstance.objects.filter(library=library, return_date__lt=date.today())

    return render(request, 'library/late_borrow_list.html', {'library': library, 'book_instances': book_instances})