# Generated by Django 4.1 on 2022-12-12 16:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_remove_library_postal_code_library_department_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='book_tile',
            new_name='book_title',
        ),
    ]
