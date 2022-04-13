from django.contrib import admin

from movielist_web_project.web.models import MovieDB, Movie, List


@admin.register(MovieDB)
class MovieDBAdmin(admin.ModelAdmin):
    list_display = ['movie_id', 'name']


@admin.register(List)
class ListOfMovies(admin.ModelAdmin):
    list_display = ['title']


@admin.register(Movie)
class Movie(admin.ModelAdmin):
    list_display = ['movie_name', 'grade']
