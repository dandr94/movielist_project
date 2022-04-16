from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
import tmdbsimple as tmdb

from movielist_web_project.accounts.models import Profile
from movielist_web_project.settings import TMDB_API_KEY
from movielist_web_project.web.models import List, Movie, MovieDB

UserModel = get_user_model()
tmdb.API_KEY = TMDB_API_KEY


class DashboardTest(TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'testuser@gmail.gg',
        'password': 'online123'
    }

    VALID_PROFILE_DATA = {
        'username': 'testuser123'
    }

    VALID_LIST_DATA = {
        'title': 'action'
    }

    VALID_LIST_DATA_2 = {
        'title': 'fantasy'
    }

    VALID_LIST_MOVIE_DATA = {
        'movie_id': 45,
        'movie_name': 'matrix',
        'grade': 5,
    }

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user)

        return user, profile

    def __create_valid_list(self, user):
        list = List.objects.create(**self.VALID_LIST_DATA, user=user)
        return list

    def __create_valid_list_and_movie(self, user):
        list = List.objects.create(**self.VALID_LIST_DATA, user=user)
        self.VALID_LIST_MOVIE_DATA['selected_list'] = list
        movie = Movie.objects.create(**self.VALID_LIST_MOVIE_DATA, user=user)
        return list, movie

    def __get_response_for_dashboard(self, **credentials):
        self.client.login(**credentials)
        return self.client.get(reverse('dashboard'))

    def test_dashboard_without_created_list_should_return_0(self):
        _, _ = self.__create_valid_user_and_profile()

        response = self.__get_response_for_dashboard(**self.VALID_USER_CREDENTIALS)

        self.assertQuerysetEqual([], response.context['lists'])

    def test_dashboard_with_created_1_list_should_return_correct_value(self):
        user, _ = self.__create_valid_user_and_profile()
        list = self.__create_valid_list(user)
        list.save()
        expected_result = ['<List: action, >']
        response = self.__get_response_for_dashboard(**self.VALID_USER_CREDENTIALS)

        self.assertQuerysetEqual(expected_result, map(repr, response.context['lists']))

    def test_dashboard_with_created_2_lists_should_return_correct_value(self):
        user, _ = self.__create_valid_user_and_profile()
        list = self.__create_valid_list(user)
        list_2 = List.objects.create(**self.VALID_LIST_DATA_2, user=user)
        list.save()
        list_2.save()
        expected_result = ['<List: action>', '<List: fantasy>']
        response = self.__get_response_for_dashboard(**self.VALID_USER_CREDENTIALS)

        self.assertQuerysetEqual(expected_result, map(repr, response.context['lists']))


class MovieDetailsTests(TestCase):
    VALID_MOVIE_CREDENTIALS = {
        'movie_id': 624860,
        'name': 'The Matrix Resurrections',
        'poster': 'https://image.tmdb.org/t/p/w500/8c4a8kE7PizaGQQnditMmI1xbRp.jpg',
        'description': "Plagued by strange memories, Neo's life takes an unexpected turn when he finds himself back inside the Matrix.",
        'duration': 148,
        'genres': 'Science Fiction, Action, Adventure',
        'average_grade': 6.8,
        'actors': "Keanu Reeves, Carrie-Anne Moss, Yahya Abdul-Mateen II, Jessica Henwick, Jonathan Groff, Neil Patrick Harris, Priyanka Chopra Jonas, Christina Ricci, Jada Pinkett Smith, Telma Hopkins",
        'roles': "Thomas A. Anderson / Neo, Tiffany / Trinity, Morpheus / Agent Smith, Bugs, Smith, The Analyst, Sati, Gwyn de Vere, Niobe, Freya",
        'production_companies': "Warner Bros. Pictures, Village Roadshow Pictures, Venus Castina Productions",
        'language': 'EN',
        'imdb_link': 'https://www.imdb.com/title/tt10838180',
        'budget': 190000000,
        'release_date': '2021-12-16',
        'status': 'Released'
    }
    VALID_USER_CREDENTIALS = {
        'email': 'testuser@gmail.gg',
        'password': 'online123'
    }
    VALID_PROFILE_DATA = {
        'username': 'testuser123'
    }


    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user)

        return user, profile

    def __get_response_for_movie_details(self, movie, **credentials):
        self.client.login(**credentials)
        return self.client.get(reverse('movie details', kwargs={'id': movie.movie_id}))

    def test_movie_details_should_return_correct_values(self):
        user, _ = self.__create_valid_user_and_profile()
        movie = MovieDB(**self.VALID_MOVIE_CREDENTIALS)
        movie.save()

        response = self.__get_response_for_movie_details(movie, **self.VALID_USER_CREDENTIALS)

        self.assertEqual(200, response.status_code)
        self.assertEqual('The Matrix Resurrections', response.context['movie'].name)
