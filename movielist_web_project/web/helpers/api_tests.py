import pprint
import requests
import tmdbsimple as tmdb

from movielist_web_project.settings import TMDB_API_KEY, YOUTUBE_SEARCH_API_KEY

tmdb.API_KEY = TMDB_API_KEY
base_url = 'https://image.tmdb.org/t/p/'
img_file_size = 'w500'
YOUTUBE_API_KEY = YOUTUBE_SEARCH_API_KEY
r = base_url + img_file_size




