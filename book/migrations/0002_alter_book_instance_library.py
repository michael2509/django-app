# Generated by Django 4.1 on 2022-12-18 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book_instance',
            name='library',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.library'),
        ),
    ]
