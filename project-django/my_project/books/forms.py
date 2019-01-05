from django import forms
from django.contrib.auth import get_user_model
from books.models import Genre, Book
from dataclasses import fields

User = get_user_model()

class CommentForm(forms.Form):
    
    comment = forms.CharField(max_length = 120, widget = forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['comment'].label = 'Новый комментарий'
        
class LoginForm(forms.Form):
    
    username = forms.CharField(max_length = 120)
    password = forms.CharField(max_length = 120, widget=forms.PasswordInput)
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        
    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('Такого пользователя не существует!')
        user = User.objects.get(username=username)
        if not user.check_password(password):
            raise forms.ValidationError('Неверный пароль!')
    
class RegistrationForm(forms.ModelForm):
    
    password_check = forms.CharField(max_length = 120, widget=forms.PasswordInput)
    password = forms.CharField(max_length = 120, widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'password_check',
            'first_name',
            'last_name',
            'email'
           ]
        
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['username'].help_text = 'Обязательное поле'
        self.fields['password'].label = 'Пароль'
        self.fields['password_check'].label = 'Подтвердите пароль'
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['email'].label = 'E-mail адрес'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким именем уже существует')
        if password != password_check:
            raise forms.ValidationError('Введенные пароли не совпадают!')
        
class NewGenreForm(forms.ModelForm):
    
    class Meta:
        model = Genre
        fields = [
            'name',
            'slug'
            ]
    
    def __init__(self, *args, **kwargs):
        super(NewGenreForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Новый жанр'
        
class NewBookForm(forms.ModelForm):
    
    class Meta:
        model = Book
        fields = [
            'genre',
            'image',
            'title',
            'author',
            'about',
            'slug',
            'cost'
            ]
        
    def __init__(self, *args, **kwargs):
        super(NewBookForm, self).__init__(*args, **kwargs)
        self.fields['genre'].label = 'Жанр'
        self.fields['image'].label = 'Изображение книги'
        self.fields['title'].label = 'Название книги'
        self.fields['author'].label = 'Автор книги'
        self.fields['about'].label = 'Содержание'
        self.fields['cost'].label = 'Стоимость'