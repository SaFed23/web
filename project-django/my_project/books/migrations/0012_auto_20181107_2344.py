# Generated by Django 2.1.2 on 2018-11-07 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0011_book_total_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='total_likes',
            field=models.FloatField(default=1.0),
        ),
    ]
