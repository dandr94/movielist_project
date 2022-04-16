from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from movielist_web_project.accounts.models import Profile
from movielist_web_project.web.models import List, Movie

UserModel = get_user_model()


class ProfileDetailsViewTest(TestCase):
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

    def __get_response_for_profile(self, profile):
        return self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))

    def test_when_valid__should_return_correct_template(self):
        user, profile = self.__create_valid_user_and_profile()
        response = self.__get_response_for_profile(profile)
        self.assertTemplateUsed('accounts/profile_details.html')

    def test_when_opening_no_existing_profile__expect_404(self):
        user, profile = self.__create_valid_user_and_profile()
        response = self.client.get(reverse('profile details', kwargs={
            'pk': 999
        }))

        self.assertEqual(404, response.status_code)

    def test_when_user_is_owner__is_owner_should_be_true(self):
        _, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.__get_response_for_profile(profile)

        self.assertTrue(response.context['is_owner'])

    def test_when_user_is_not_owner__is_owner__should_be_false(self):  # FIX THIS
        user, profile = self.__create_valid_user_and_profile()
        credentials = {
            'email': 'testuser2@gmail.bb',
            'password': 'online321'
        }
        self.__create_user(**credentials)

        self.client.login(**credentials)

        response = self.__get_response_for_profile(profile)
        h = response.context['is_owner']


        self.assertFalse(response.context['is_owner'])

    def test_when_no_movies__total_movies_count_should_be_0(self):
        user, profile = self.__create_valid_user_and_profile()
        list = self.__create_valid_list(user)

        response = self.__get_response_for_profile(profile)

        self.assertEqual(0, response.context['all_movies_count'])

    def test_when_there_are_movies__total_movies_should_be_correct_value(self):
        user, profile = self.__create_valid_user_and_profile()
        list, movie = self.__create_valid_list_and_movie(user)
        movie.save()

        response = self.__get_response_for_profile(profile)

        self.assertEqual(1, response.context['all_movies_count'])

    def test_when_no_lists__total_lists_count_should_be_0(self):
        _, profile = self.__create_valid_user_and_profile()

        response = self.__get_response_for_profile(profile)

        self.assertEqual(0, response.context['all_lists_count'])

    def test_when_there_are_lists__total_lists_should_be_correct_value(self):
        user, profile = self.__create_valid_user_and_profile()
        list = self.__create_valid_list(user)

        response = self.__get_response_for_profile(profile)

        self.assertEqual(1, response.context['all_lists_count'])

    def test_when_user_has_lists__should_return_only_his_lists(self):
        user, profile = self.__create_valid_user_and_profile()
        credentials = {
            'email': 'testuser2@gmail.gg',
            'password': 'online5573'
        }
        list = self.__create_valid_list(user)

        user_2 = self.__create_user(**credentials)
        self.__create_valid_list(user_2)

        response = self.__get_response_for_profile(profile)

        self.assertCountEqual(
            [list],
            response.context['all_lists']
        )

    def test_when_no_average_grade__total_average_grade_count_should_be_0(self):
        user, profile = self.__create_valid_user_and_profile()
        list = self.__create_valid_list(user)

        response = self.__get_response_for_profile(profile)

        self.assertEqual(0, response.context['average_grade'])

    def test_when_there_is_average_grade__total_average_grade_should_be_correct_value(self):
        user, profile = self.__create_valid_user_and_profile()
        list, movie = self.__create_valid_list_and_movie(user)
        movie.save()

        response = self.__get_response_for_profile(profile)

        self.assertEqual('5.00', response.context['average_grade'])

    def test_individual_list_in_your_list_category(self):
        user, profile = self.__create_valid_user_and_profile()
        list, movie = self.__create_valid_list_and_movie(user)
        movie.save()
        expected_result = {
            'action': {
                'average_grade': "5.00",
                'total_movies': 1
            }
        }
        response = self.__get_response_for_profile(profile)

        self.assertEqual(1, len(response.context['lists']))

