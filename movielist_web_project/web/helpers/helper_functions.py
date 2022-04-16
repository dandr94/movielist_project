import tmdbsimple as tmdb
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
import requests

from movielist_web_project.settings import TMDB_API_KEY, YOUTUBE_SEARCH_API_KEY
from movielist_web_project.web.models import MovieDB

UserModel = get_user_model()
tmdb.API_KEY = TMDB_API_KEY
TMDB_IMG_PATH = 'https://image.tmdb.org/t/p/w500'
YOUTUBE_SEARCH_PATH = 'https://www.googleapis.com/youtube/v3/search'
YOUTUBE_BASIC_PATH = 'https://www.youtube.com/watch?v='
YOUTUBE_ADDITIONAL_QUERY_SEARCH_WORD = 'trailer'
YOUTUBE_MAX_RESULT_PAGES = 1
YOUTUBE_SEARCH_TYPE = 'video'
YOUTUBE_API_KEY = YOUTUBE_SEARCH_API_KEY
IMDB_PATH = 'https://www.imdb.com/title/'


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
        'poster': TMDB_IMG_PATH + info['poster_path'],
        'description': info['overview'],
        'duration': info['runtime'],
        'genres': ", ".join([g['name'] for g in info['genres']]),
        'average_grade': info['vote_average'],
        'actors': ", ".join([cast['name'] for cast in movie.credits()['cast'][:10]]),
        'roles': ", ".join([cast['character'] for cast in movie.credits()['cast'][:10]]),
        'production_companies': ", ".join([c['name'] for c in info['production_companies']]),
        'language': info['original_language'].upper(),
        'imdb_link': IMDB_PATH + info['imdb_id'],
        'budget': info['budget'],
        'release_date': info['release_date'],
        'status': info['status']

    }

    MovieDB(**data).save()


def return_youtube_trailer(movie_name: str, release_date: str) -> str:
    search_url: str = YOUTUBE_SEARCH_PATH
    basic_path: str = YOUTUBE_BASIC_PATH
    query_params: str = movie_name + " " + release_date + " " + YOUTUBE_ADDITIONAL_QUERY_SEARCH_WORD

    search_params = {
        'part': 'snippet',
        'q': query_params,
        'key': YOUTUBE_API_KEY,
        'maxResults': YOUTUBE_MAX_RESULT_PAGES,
        'type': YOUTUBE_SEARCH_TYPE
    }

    search_result = requests.get(search_url, params=search_params)
    json_result = search_result.json()['items']
    for result in json_result:
        return basic_path + result['id']['videoId']


def return_list_with_additional_stats(lists: list, movies: list) -> dict:
    data: dict = {}

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
