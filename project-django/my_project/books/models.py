from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from sqlite3 import Timestamp
from django.template.defaultfilters import default
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation


def generate_filename(instance, filename):
    filename = instance.slug + '.jpg'
    return "{0}/{1}".format(instance, filename)
    

class Genre(models.Model):
    
    name = models.CharField(max_length = 50)
    slug = models.SlugField()

    def __str__(self):
        return "Жанр книги '{0}'".format(self.name)

    def get_absolute_url(self):
        return reverse("genre-detail", kwargs={"slug": self.slug})

class Book(models.Model):
    
    genre = models.ForeignKey(Genre, '')
    image = models.ImageField(upload_to = generate_filename)
    slug = models.SlugField()
    title = models.CharField(max_length = 120) 
    author = models.CharField(max_length = 120)
    about = models.TextField()
    cost = models.FloatField()
    likes = models.PositiveIntegerField(default = 0)
    dislikes = models.PositiveIntegerField(default = 0)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    comments = GenericRelation('comments')
    user_reaction = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True )
    total_likes = models.FloatField(default = 0)
    total_number = models.PositiveIntegerField(default = 0)
    
    def print_t_l(self):
        if (self.dislikes + self.likes) != 0:
            self.total_likes = self.likes * 5 /(self.dislikes + self.likes)
        else:
            self.total_likes = -1
        self.save()
        return self.total_likes
    
    def __str__(self):
        return "Книга '{0}' жанра '{1}'".format(self.title, self.genre.name)

    def get_absolute_url(self):
        return reverse("book-detail", kwargs={ "genre": self.genre.slug,"slug": self.slug})
    

class Comments(models.Model):
    
    author = models.ForeignKey(settings.AUTH_USER_MODEL, '')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    content_type = models.ForeignKey(ContentType, '')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    def __str__(self):
        return "Комментарий автора '{0}'".format(self.author)
    
class UserAccount(models.Model):
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, '')
    first_name = models.CharField(max_length = 120)
    last_name = models.CharField(max_length = 120)
    email = models.EmailField()
    user_books = models.ManyToManyField(Book, blank = True)
    
    def total_cost(self):
        total_cost = 0
        for book in self.user_books.all():
            total_cost += book.cost * book.total_number
        return round(total_cost, 2)
    
    def __str__(self):
        return self.user.username
    
    def get_absolute_url(self):
        return reverse("account-view", kwargs={ "user": self.user.username})