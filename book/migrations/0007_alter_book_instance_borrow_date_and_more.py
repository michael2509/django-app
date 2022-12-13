# Generated by Django 4.1 on 2022-12-12 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0006_rename_name_book_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book_instance',
            name='borrow_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='date borrowed'),
        ),
        migrations.AlterField(
            model_name='book_instance',
            name='return_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='date returned'),
        ),
    ]
