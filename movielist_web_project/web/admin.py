from django.contrib import admin

from movielist_web_project.web.models import MovieDB, Movie, List


@admin.register(MovieDB)
class MovieDBAdmin(admin.ModelAdmin):
    list_display = ['movie_id', 'name', 'poster', 'description', 'duration', 'genres', 'average_grade', 'actors', 'roles', 'production_companies', 'language', 'imdb_link', 'budget', 'release_date', 'status']


@admin.register(List)
class ListOfMovies(admin.ModelAdmin):
    list_display = ['title', 'user']
    exclude = ['user']


@admin.register(Movie)
class Movie(admin.ModelAdmin):
    list_display = ['movie_name', 'selected_list', 'user', 'grade', 'would_recommend']
    exclude = ['user']
