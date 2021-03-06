# Generated by Django 2.1.2 on 2018-11-11 16:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0016_book_total_likes'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=120)),
                ('last_name', models.CharField(max_length=120)),
                ('email', models.EmailField(max_length=254)),
                ('user', models.OneToOneField(on_delete='', to=settings.AUTH_USER_MODEL)),
                ('user_books', models.ManyToManyField(to='books.Book')),
            ],
        ),
    ]
