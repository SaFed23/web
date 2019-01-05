from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from books.models import Book, Genre, Comments, UserAccount
from books.mixins import GenreListMixin
from django.http.response import JsonResponse, HttpResponseRedirect
from books.forms import CommentForm, RegistrationForm, LoginForm, NewGenreForm, NewBookForm
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.db.models import Q
from django.template.context_processors import request

def generate_filename(instance, filename):
    filename = instance.slug + '.jpg'
    return "{0}/{1}".format(instance, filename)

class InfoView(ListView):
    model = Genre
    template_name = "../../mainwindow/templates/mainwindow/info.html"
    
    def get_context_data(self, *args, **kwargs):
        context = super(InfoView, self).get_context_data(*args, **kwargs)
        context['genres'] = self.model.objects.all()
        return context

class BookListView(ListView, GenreListMixin):
    model = Book
    template_name = "../../mainwindow/templates/mainwindow/books.html"

    def get_context_data(self, *args, **kwargs):
        context = super(BookListView, self).get_context_data(*args, **kwargs)
        context['books'] = self.model.objects.order_by('title').all()
        return context
    

class GenreListView(ListView):
    model = Genre
    template_name = "../../mainwindow/templates/mainwindow/homePage.html"

    def get_context_data(self, *args, **kwargs):
        context = super(GenreListView, self).get_context_data(*args, **kwargs)
        context['slider_books'] = Book.objects.all().order_by('-timestamp')[:5]
        context['genres'] = self.model.objects.all()
        return context
        
class GenreDetailView(DetailView, GenreListMixin):
    
    model = Genre
    template_name = "../../mainwindow/templates/mainwindow/genre.html"

    def get_context_data(self, *args, **kwargs):
        context = super(GenreDetailView, self).get_context_data(*args, **kwargs)
        context['genre'] = self.get_object()
        context['book_from_genre'] = self.get_object().book_set.all()
        return context
    
class BookDetailView(DetailView, GenreListMixin):
    
    model = Book
    template_name = "../../mainwindow/templates/mainwindow/book.html"

    def get_context_data(self, *args, **kwargs):
        context = super(BookDetailView, self).get_context_data(*args, **kwargs)
        context['book'] = self.get_object()
        context['book_comments'] = self.get_object().comments.all()
        context['form'] = CommentForm()
        return context
    
class CreateCommentView(View):
    
    template_name = "../../mainwindow/templates/mainwindow/book.html"
    
    def post(self, request, *args, **kwargs):
        User = get_user_model()
        book_id = self.request.POST.get('book_id')
        comment = self.request.POST.get('comment')
        book = Book.objects.get(id=book_id)
        new_comment = book.comments.create(author = request.user, content = comment)
        comment = [{'author': new_comment.author.username, 'comment': new_comment.content, 'timestamp': new_comment.timestamp.strftime('%Y-%m-%d')}]
        return JsonResponse(comment, safe=False)
        
class UserLikesView(View):
    
    temlate_name = "../../mainwindow/templates/mainwindow/book.html" 
    
    def get(self, request, *args, **kwargs):
        book_id = self.request.GET.get('book_id')
        book = Book.objects.get(id=book_id)
        like = self.request.GET.get('like')
        dislike = self.request.GET.get('dislike')
        if like and (request.user not in book.user_reaction.all()):
            book.likes += 1
            book.user_reaction.add(request.user)
            book.save()
        if dislike and (request.user not in book.user_reaction.all()):
            book.dislikes += 1
            book.user_reaction.add(request.user)
            book.save()
        data = {
            'likes': book.likes,
            'dislikes':book.dislikes
            }
        return JsonResponse(data)
    
class RegistrationView(View):
    
    model = Genre
    template_name = "../../mainwindow/templates/mainwindow/registration.html"

    def get(self, request, *args, **kwargs):
        form = RegistrationForm()
        context = {
            'form': form,
            'genres': self.model.objects.all()
            }
        return render(self.request, self.template_name, context)
    
    def post(self, request, *args, **kargs):
        User = get_user_model()
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            new_user.set_password(password)
            password_check = form.cleaned_data['password_check']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            new_user.save()
            UserAccount.objects.create(user = User.objects.get(username=new_user.username),
                                       first_name = new_user.first_name,
                                       last_name = new_user.last_name,
                                       email = new_user.email)
            return HttpResponseRedirect('/')
        context = {
            'form' : form,
            'genres' : self.model.objects.all()
        }
        return render(self.request, self.template_name, context)
    
class LoginView(View, GenreListMixin):
    
    model = Genre
    template_name = "../../mainwindow/templates/mainwindow/login.html"

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        context = {
            'form': form,
            'genres': self.model.objects.all()
            }
        return render(self.request, self.template_name, context)
    
    def post(self, request, *args, **kargs):
        User = get_user_model()
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(self.request, user)
                return HttpResponseRedirect('/')
        context = {
            'form' : form,
            'genres' : self.model.objects.all()
        }
        return render(self.request, self.template_name, context)
    
class UserAccountView(View):
    
    model = Genre
    template_name = "../../mainwindow/templates/mainwindow/user_account.html"
    
    def get(self, request, *args, **kwargs):
        User = get_user_model()
        user = self.kwargs.get('user') 
        current_user = UserAccount.objects.get(user = User.objects.get(username = user))
        context = {
            'genres' : self.model.objects.all(),
            'current_user' : current_user
            }
        return render(self.request, self.template_name, context)          
    
class BuyBook(View):
    
    template_name = "../../mainwindow/templates/mainwindow/book.html"
    
    def get(self, request, *args, **kargs):
        book_slug = self.request.GET.get('book_slug')
        book = Book.objects.get(slug = book_slug)
        current_user = UserAccount.objects.get(user = request.user)
        current_user.user_books.add(book)
        book = current_user.user_books.get(slug=book_slug)
        book.total_number += 1
        book.save()
        current_user.save()
        return JsonResponse({'ok':'ok'})
    
class DeleteBook(View):
    
    template_name = "../../mainwindow/templates/mainwindow/user_account.html"
    
    def get(self, request, *args, **kargs):
        book_slug = self.request.GET.get('book_slug')
        book = Book.objects.get(slug = book_slug)
        current_user = UserAccount.objects.get(user = request.user)
        book = current_user.user_books.get(slug=book_slug)
        book.total_number -= 1
        book.save()
        if not book.total_number:
            current_user.user_books.remove(book)
        current_user.save()
        return JsonResponse({'ok':'ok'})
    
class SearchView(View):
    
    template_name = "../../mainwindow/templates/mainwindow/search.html"
    
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        founded_books = Book.objects.filter(
            Q(title__icontains=query)|
            Q(author__icontains=query))
        context = {
            'genres' : Genre.objects.all(),
            'founded_books' : founded_books
            }
        return render(self.request, self.template_name, context)
    
class RegistretionNewGenre(View):
    
    model = Genre
    template_name = "../../mainwindow/templates/mainwindow/registration_genre.html"

    def get(self, request, *args, **kwargs):
        form = NewGenreForm()
        context = {
            'form': form,
            'genres': self.model.objects.all()
            }
        return render(self.request, self.template_name, context)
    
    def post(self, request, *args, **kargs):
        form = NewGenreForm(request.POST or None)
        if form.is_valid():
            new_genre = form.save(commit=False)
            name = form.cleaned_data['name']
            slug = form.cleaned_data['slug']
            Genre.objects.create(name = new_genre.name,
                                 slug = new_genre.slug)
            return HttpResponseRedirect('/')
        context = {
            'form' : form,
            'genres' : self.model.objects.all()
        }
        return render(self.request, self.template_name, context)
    
class RegistrationNewBook(View):
    
    model = Genre
    template_name = "../../mainwindow/templates/mainwindow/registration_book.html"

    def get(self, request, *args, **kwargs):
        form = NewBookForm()
        context = {
            'form': form,
            'genres': self.model.objects.all()
            }
        return render(self.request, self.template_name, context)
    
    def post(self, request, *args, **kargs):
        form = NewBookForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            author = form.cleaned_data['author']
            image = form.cleaned_data['image']
            about = form.cleaned_data['about']
            cost = form.cleaned_data['cost']
            genre = form.cleaned_data['genre']
            slug = form.cleaned_data['slug']
            Book.objects.create(title = title,
                                image = image,
                                author = author,
                                about = about,
                                cost = cost,
                                genre = genre,
                                slug = slug
                                 )
            return HttpResponseRedirect('/')
        context = {
            'form' : form,
            'genres' : self.model.objects.all()
        }
        return render(self.request, self.template_name, context)

class DeleteBookShop(View):
    
    template_name = "../../mainwindow/templates/mainwindow/books.html"
    
    def get(self, request, *args, **kargs):
        book_slug = self.request.GET.get('book_slug')
        book = Book.objects.get(slug = book_slug)
        book.delete()
        return JsonResponse({'ok':'ok'})
    
class DeleteGenre(View):
    
    template_name = "../../mainwindow/templates/mainwindow/wrapper.html"
    
    def get(self, request, *args, **kargs):
        genre_slug = self.request.GET.get('genre_slug')
        genre = Genre.objects.get(slug = genre_slug)
        book = Book.objects.filter(genre = genre.id).delete()
        genre.delete()
        return JsonResponse({'ok':'ok'})
    
class AccountAllView(View):
    
    model = Genre
    template_name = "../../mainwindow/templates/mainwindow/account_all.html"
    
    def get(self, request, *args, **kwargs):
        context = {
            'genres' : self.model.objects.all(),
            'current_user' : UserAccount.objects.all()
            }
        return render(self.request, self.template_name, context) 
    
class AccountDeleteView(View):
    
    template_name = "../../mainwindow/templates/mainwindow/account_all.html"
    
    def get(self, request, *args, **kargs):
        user = self.request.GET.get('user')
        User = get_user_model()
        user_delete = User.objects.get(username = user)
        UserAccount.objects.get(user = user_delete).delete()
        user_delete.delete()
        return JsonResponse({'ok':'ok'})

class CommentDeleteView(View):
    
    template_name = "../../mainwindow/templates/mainwindow/book.html"
    
    def get(self, request, *args, **kargs):
        id = self.request.GET.get('id')
        Comments.objects.filter(id = id).delete()
        return JsonResponse({'ok':'ok'})