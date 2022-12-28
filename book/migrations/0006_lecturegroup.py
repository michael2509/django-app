# Generated by Django 4.1 on 2022-12-28 14:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('book', '0005_alter_bookinstance_borrow_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='LectureGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='date of the meeting')),
                ('library', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.library')),
                ('participants', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
