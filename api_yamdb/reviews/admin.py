from django.contrib import admin

from .models import Categories, Comment, Genres, GenreTitle, Review, Title

admin.site.register(Comment)
admin.site.register(Review)


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre',)
    list_filter = ('genre',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('year', 'category', 'genre', 'name',)
