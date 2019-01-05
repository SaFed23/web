from django.urls import path, include
from . import views
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout
from books.views import (
    BookListView,
    GenreListView, 
    GenreDetailView, 
    BookDetailView, 
    CreateCommentView, 
    InfoView,
    UserLikesView,
    RegistrationView,
    LoginView,
    UserAccountView,
    BuyBook,
    DeleteBook,
    SearchView,
    RegistretionNewGenre,
    RegistrationNewBook,
    DeleteBookShop,
    DeleteGenre,
    AccountAllView,
    AccountDeleteView,
    CommentDeleteView)

urlpatterns = [
    path('', GenreListView.as_view(), name = 'home'),
    path('delete_genre/', DeleteGenre.as_view(), name='delete_genre'),
    path('genre/<slug>/', GenreDetailView.as_view(), name = 'genre-detail'),
    path('user_account/<user>/', UserAccountView.as_view(), name = 'account-view'),
    path('<genre>/<slug>/', BookDetailView.as_view(), name = 'book-detail'),
    path('add_comment/', CreateCommentView.as_view(), name = 'add_comment'),
    path('user_likes/', UserLikesView.as_view(), name = 'user_likes'),
    path('books/', BookListView.as_view(), name='books'),
    path('info/', InfoView.as_view(), name = 'info'),
    path('registration/', RegistrationView.as_view(), name = 'registration'),
    path('login/', LoginView.as_view(), name = 'login'),
    path('buy_book/', BuyBook.as_view(), name = 'buy_book'),
    path('delete_book/', DeleteBook.as_view(), name = 'delete_book'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('home')), name='logout_view'),
    path('search', SearchView.as_view(), name='search'),
    path('new_genre/', RegistretionNewGenre.as_view(), name='new_genre'),
    path('new_book/', RegistrationNewBook.as_view(), name='new_book'),
    path('delete_book_shop/', DeleteBookShop.as_view(), name='del_book_shop'),
    path('account_all/', AccountAllView.as_view(), name='account_all'),
    path('delete_user/', AccountDeleteView.as_view(), name='delete_user'),
    path('delete_comment/', CommentDeleteView.as_view(), name='delete_comment')
]
