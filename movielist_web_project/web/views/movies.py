import tmdbsimple as tmdb
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from movielist_web_project.settings import TMDB_API_KEY
from movielist_web_project.web.forms import AddMovieToListForm
from movielist_web_project.web.helpers.helper_functions import check_if_in_db, return_youtube_trailer
from movielist_web_project.web.models import MovieDB, List

UserModel = get_user_model()
tmdb.API_KEY = TMDB_API_KEY
img_path = 'https://image.tmdb.org/t/p/w500/'
img_not_found = 'https://westsiderc.org/wp-content/uploads/2019/08/Image-Not-Available.png'


@login_required(login_url='login user')
def show_search_page(request):
    movies = []
    if request.method == 'POST':
        keyword = request.POST['search']

        if keyword == '':
            return redirect('movie search')

        search_params = {
            'query': keyword,
            'page': 1,
        }
        search = tmdb.Search()
        response = search.movie(**search_params)

        for item in response['results']:
            item_result = {
                'title': item['title'],
                'vote_average': item['vote_average'],
                'image': img_path + item['poster_path'] if item['poster_path'] else img_not_found,
                'id': item['id'],
            }

            movies.append(item_result)

    context = {
        'movies': movies,
        'hide_footer': True
    }

    return render(request, 'main/movie_search.html', context)


class MovieDetailsView(LoginRequiredMixin, TemplateView):
    template_name = 'main/movie_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie = check_if_in_db(kwargs['id'])
        context['movie'] = movie
        context['trailer'] = return_youtube_trailer(movie.name, str(movie.release_date.year))
        return context


@login_required(login_url='login user')
def add_movie_to_list(request, pk):
    movie = MovieDB.objects.get(pk=pk)
    lists = List.objects.filter(user_id=request.user.id)

    if request.method == 'POST':
        try:
            form = AddMovieToListForm(movie, request.user.id, lists, request.POST)

            if form.is_valid():
                form.save()

            return redirect('movie search')
        except IntegrityError:  # fix
            return redirect('movie search')
    else:
        form = AddMovieToListForm(movie, request.user.id, lists)

    context = {
        'form': form,
        'movie': movie,
        'hide_header': True,
        'hide_footer': True

    }

    return render(request, 'main/movie_add_to_list.html', context)
