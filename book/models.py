from django.db import models
from accounts.models import User

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=80)
    editor = models.CharField(max_length=80)
    genre = models.CharField(max_length=30)
    cover = models.ImageField(upload_to='images/', null=True, blank=True)
    # pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.title


class BookInstance(models.Model):
    # ForeignKey => many-to-one: one book_instance can have only one book but one book can have many book_instances
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    library = models.ForeignKey('Library', on_delete=models.CASCADE)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)
    borrow_date = models.DateTimeField('date borrowed', null=True, blank=True)
    return_date = models.DateTimeField('date returned', null=True, blank=True)

    def __str__(self):
        return "%s (bibliothèque : %s)" % (self.book, self.library)


class Library(models.Model):
    name = models.CharField(max_length=200, default="Bibliothèque sans nom")
    adress = models.CharField(max_length=200)
    department_code = models.IntegerField(default=75)
    owners = models.ManyToManyField(User)

    def __str__(self):
        return self.name