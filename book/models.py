from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=80)
    editor = models.CharField(max_length=80)
    genre = models.CharField(max_length=30)
    cover = models.CharField(max_length=100)
    # pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.title


class Book_instance(models.Model):
    # ForeignKey => many-to-one: one book_instance can have only one book but one book can have many book_instances
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    library = models.OneToOneField('Library', on_delete=models.CASCADE)
    # TODO: add this field when our authentification system is ready
    # borrower = models.OneToOneField('User', on_delete=models.CASCADE, default=None)
    borrow_date = models.DateTimeField('date borrowed', null=True, blank=True)
    return_date = models.DateTimeField('date returned', null=True, blank=True)

    def __str__(self):
        return "%s chez %s" % (self.book, self.library)


class Library(models.Model):
    name = models.CharField(max_length=200, default="Bibliothèque sans nom")
    adress = models.CharField(max_length=200)
    department_code = models.IntegerField(default=75)
    # TODO: add this field when our authentification system is ready
    # owners = models.ManyToManyField('User')

    def __str__(self):
        return self.name