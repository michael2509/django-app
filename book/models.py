from django.db import models


class Book(models.Model):
    book_title = models.CharField(max_length=200)
    book_author = models.CharField(max_length=80)
    book_editor = models.CharField(max_length=80)
    book_genre = models.CharField(max_length=30)
    book_cover = models.CharField(max_length=100)
    # pub_date = models.DateTimeField('date published')


class Book_instance(models.Model):
    # ForeignKey => many-to-one: one book_instance can have only one book but one book can have many book_instances
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    library = models.OneToOneField('Library', on_delete=models.CASCADE)
    # TODO: add this field when our authentification system is ready
    # borrower = models.OneToOneField('User', on_delete=models.CASCADE, default=None)
    borrow_date = models.DateTimeField('date borrowed')
    return_date = models.DateTimeField('date returned')


class Library(models.Model):
    adress = models.CharField(max_length=200)
    # TODO: add this field when our authentification system is ready
    # owners = models.ManyToManyField('User')

    def __str__(self):
        return "%s the library" % self.adress