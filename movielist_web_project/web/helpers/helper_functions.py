import tmdbsimple as tmdb
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
import requests

from movielist_web_project.settings import TMDB_API_KEY, YOUTUBE_SEARCH_API_KEY
from movielist_web_project.web.models import MovieDB

UserModel = get_user_model()
tmdb.API_KEY = TMDB_API_KEY
img_path = 'https://image.tmdb.org/t/p/w500'
imdb_path = 'https://www.imdb.com/title/'
YOUTUBE_API_KEY = YOUTUBE_SEARCH_API_KEY


def check_if_in_db(movie_id: int) -> object:
    try:
        movie = MovieDB.objects.get(movie_id=movie_id)
        return movie
    except ObjectDoesNotExist:
        add_movie_to_db(movie_id)
        get_movie = MovieDB.objects.get(movie_id=movie_id)
        return get_movie


def add_movie_to_db(movie_id: int):
    movie = tmdb.Movies(movie_id)
    info = movie.info()

    data = {
        'movie_id': movie_id,
        'name': info['title'],
        'poster': img_path + info['poster_path'],
        'description': info['overview'],
        'duration': info['runtime'],
        'genres': ", ".join([g['name'] for g in info['genres']]),
        'average_grade': info['vote_average'],
        'actors': ", ".join([cast['name'] for cast in movie.credits()['cast'][:10]]),
        'roles': ", ".join([cast['character'] for cast in movie.credits()['cast'][:10]]),
        'production_companies': ", ".join([c['name'] for c in info['production_companies']]),
        'language': info['original_language'].upper(),
        'imdb_link': imdb_path + info['imdb_id'],
        'budget': info['budget'],
        'release_date': info['release_date'],
        'status': info['status']

    }

    MovieDB(**data).save()


def return_youtube_trailer(movie_name: str, release_date: str) -> str:
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    basic_path = 'https://www.youtube.com/watch?v='
    query_params = movie_name + " " + release_date + " " + 'trailer'

    search_params: dict = {
        'part': 'snippet',
        'q': movie_name + query_params,
        'key': YOUTUBE_API_KEY,
        'maxResults': 1,
        'type': 'video'
    }

    search_result = requests.get(search_url, params=search_params)
    json_result = search_result.json()['items']
    for result in json_result:
        return basic_path + result['id']['videoId']


def return_list_with_additional_stats(lists: list, movies: list) -> dict:
    data = {}

    for l in lists:
        data[l] = {'average_grade': "", 'total_movies': 0}
        grades = 0
        total_movies = 0
        for movie in movies:
            if movie.selected_list_id == l.id:
                grades += movie.grade
                total_movies += 1

        if total_movies:
            data[l]['total_movies'] += total_movies
            data[l]['average_grade'] = f'{grades / total_movies:.2f}'
        else:
            data[l]['total_movies'] = 0
            data[l]['average_grade'] = 0

    return data
