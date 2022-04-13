from django.urls import path

from movielist_web_project.web.views.generic import HomeViewNoProfile, Dashboard, AboutView
from movielist_web_project.web.views.movie_list import DeleteMovieFromMovieList, \
    CreateMovieListView, EditMovieListView, DeleteMovieListView, DetailsMovieListView
from movielist_web_project.web.views.movies import show_search_page, MovieDetailsView, add_movie_to_list

urlpatterns = [
    path('', HomeViewNoProfile.as_view(), name='index'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('about/', AboutView.as_view(), name='about'),


    path('list/add', CreateMovieListView.as_view(), name='create list'),
    path('list/edit/<int:pk>/', EditMovieListView.as_view(), name='edit list'),
    path('list/delete/<int:pk>/', DeleteMovieListView.as_view(), name='delete list'),
    path('list/details/<int:pk>', DetailsMovieListView.as_view(), name='details list'),
    path('list/movie/delete/<int:pk>', DeleteMovieFromMovieList.as_view(), name='mvl movie delete'),


    path('movie/add/<int:pk>', add_movie_to_list, name='add movie to list'),
    path('movie/details/<id>', MovieDetailsView.as_view(), name='movie details'),
    path('movie/search/', show_search_page, name='movie search'),
]


