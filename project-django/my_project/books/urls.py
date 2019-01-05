from django.urls import path, include
from django.views.generic import ListView, DetailView
from books.models import Genre, Book
from . import views
