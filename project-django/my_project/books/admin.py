from django.contrib import admin
from books.models import Genre, Book, Comments, UserAccount

class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Genre)
admin.site.register(Book, BookAdmin)
admin.site.register(Comments)
admin.site.register(UserAccount)