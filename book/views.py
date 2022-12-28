from django.shortcuts import get_object_or_404, render
from .models import LectureGroup, Library, BookInstance, Message
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import AddBookForm, BorrowBookForm, CreateLectureGroupForm, SendMessageForm
from .decorators import owner_required, bookseller_required
from datetime import date
from django.contrib.auth.decorators import login_required


def home(request):
    book_instances = None
    lecture_groups = None

    if request.user.is_authenticated and request.user.role == 'customer':
        book_instances = BookInstance.objects.filter(borrower=request.user, return_date__lt=date.today())
        lecture_groups = LectureGroup.objects.filter(participants=request.user)

    return render(request, 'book/index.html', {'user': request.user, 'book_instances': book_instances, 'lecture_groups': lecture_groups})

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

        books_infos = []
        for book_instance in book_instances:
            if not any(book_info['book'].title == book_instance.book.title for book_info in books_infos):
                books_infos.append({'book': book_instance.book, 'libraries': []})
                all_libraries = Library.objects.all()
                for library in all_libraries:
                    if not BookInstance.objects.filter(book=book_instance.book, library=library, borrower__isnull=False):
                        books_infos[-1]['libraries'].append({'library': library, 'available': True})
                    else:
                        books_infos[-1]['libraries'].append({'library': library, 'available': False})

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

@owner_required
def lecture_group(request, library_id):
    library = get_object_or_404(Library, id=library_id)

    if request.method == 'GET':
        lecture_group_form = CreateLectureGroupForm(initial={'library': library})
        lecture_groups = LectureGroup.objects.filter(library=library).order_by('startDateTime')
        
        return render(request, 'library/lecture_group.html', {'library': library, 'lecture_group_form': lecture_group_form, 'lecture_groups': lecture_groups})

    if request.method == 'POST':
        lecture_group_form = CreateLectureGroupForm(request.POST)
        lecture_groups = LectureGroup.objects.filter(library=library).order_by('startDateTime')

        if lecture_group_form.is_valid():
            lecture_group_form.save()
            messages.success(request, 'Groupe de lecture créé')
        else:
            messages.error(request, 'Erreur durant la création du groupe de lecture')
        
        return render(request, 'library/lecture_group.html', {'library': library, 'lecture_group_form': lecture_group_form, 'lecture_groups': lecture_groups})


@login_required
def chat(request):
    
    if request.method == 'GET':
        chat_messages = Message.objects.filter().order_by('-creationDateTime')
        message_form = SendMessageForm(initial={'sender': request.user})

        return render(request, 'book/chat.html', {'chat_messages': chat_messages, 'message_form': message_form})

    if request.method == 'POST':
        message_form = SendMessageForm(request.POST)
        chat_messages = Message.objects.filter().order_by('-creationDateTime')

        if message_form.is_valid():
            message_form.save()
            messages.success(request, 'Message envoyé')
        else:
            messages.error(request, 'Erreur durant l\'envoi du message')

        return render(request, 'book/chat.html', {'chat_messages': chat_messages, 'message_form': message_form})