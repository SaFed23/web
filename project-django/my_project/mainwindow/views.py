from django.shortcuts import render
from books.models import Book
from books.views import GenreListView

def homePage(request):
    return render(request, 'mainwindow/homePage.html')

def booksPage(request):
    return render(request, 'mainwindow/books.html')

def infoPage(request):
    return render(request, 'mainwindow/info.html')
