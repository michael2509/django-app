from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404, render
from .models import Book, Library, BookInstance, User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .forms import AddBookForm, BorrowBookForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def index(request):
    book_list = get_list_or_404(Book) 

    context = {
        'book_list': book_list,
    }
    return render(request, 'book/index.html', context)


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

        return render(request, 'book/search.html', {'book_instances': book_instances})
    else:
        return render(request, 'book/search.html')


class AddBook(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    form_class = AddBookForm
    success_url = reverse_lazy("add_book")
    template_name = "book/add_book.html"

    # allow this views only to users with role bookseller
    def test_func(self):
        print(self.request.user.role)
        return self.request.user.role == 'bookseller'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully')
            return render(request, self.template_name, {'form': form})
        else:
            messages.error(request, 'Error adding book')
            return render(request , self.template_name, {'form': form})

    def get(self, request, *args, **kwargs):
        form = self.form_class(user=request.user)
        return render(request , self.template_name, {'form': form})

def libraries_owned(request):
    libraries = Library.objects.filter(owners=request.user)
    return render(request, 'library/libraries_owned.html', {'libraries': libraries})

def library(request, library_id):
    if request.user.role == 'bookseller' and request.user not in library.owners.all():
        return HttpResponse("You don't have permission to view this library")
    
    library = get_object_or_404(Library, id=library_id)

    # search book
    if request.GET.get('book_name'):
        print('searching book')
        users = User.objects.all()
        book_name = request.GET.get('book_name')
        book_instances = BookInstance.objects.filter(library=library, book__title__icontains=book_name)
        book_instances = sorted(book_instances, key=lambda x: (x.book.title, x.borrower is None), reverse=True)
        book_instances = [book_instances[i] for i in range(len(book_instances)) if i == 0 or book_instances[i].book.title != book_instances[i-1].book.title]

        borrow_form = BorrowBookForm()

        return render(request, 'library/library.html', {'library': library, 'book_instances': book_instances, 'users': users, 'borrow_form': borrow_form})

    return render(request, 'library/library.html', {'library': library})

def borrow_book(request, library_id):
    if request.method == 'POST':
        print('borrowing book')
        library = get_object_or_404(Library, id=library_id)
        book_instance_id = request.POST.get('book_instance_id')
        book_instance = get_object_or_404(BookInstance, id=book_instance_id)
        borrow_form = BorrowBookForm(request.POST, instance=book_instance)

        if borrow_form.is_valid():
            borrow_form.save()
            messages.success(request, 'Book borrowed successfully')
        else:
            print(borrow_form.errors)
            messages.error(request, 'Error borrowing book')

    return redirect('library', library_id=library_id)
