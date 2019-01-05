from django.views.generic.list import MultipleObjectMixin
from books.models import Genre
from crispy_forms.tests import forms

class GenreListMixin(MultipleObjectMixin):
    
    def get_context_data(self, *args, **kwargs):
        context = {}
        context['genres'] = Genre.objects.all() 
        return context
    
    
    