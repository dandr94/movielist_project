from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.db import IntegrityError
from django.shortcuts import redirect

from movielist_web_project.web.models import Movie, List

UserModel = get_user_model()


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        max_length=100
    )
    password = forms.CharField(
        max_length=100
    )

    class Meta:
        model = UserModel
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'placeholder': 'Email',
                    'class': 'sign__input',
                }
            ),
            'password': forms.PasswordInput(
                attrs={
                    'placeholder': 'Password',
                    'class': 'sign__input'
                }
            )
        }


class CreateListForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        m_list = super().save(commit=False)

        m_list.user = self.user
        if commit:
            try:
                m_list.save()
            except IntegrityError:  # << FIX
                return redirect('dashboard')

        return m_list

    class Meta:
        model = List
        fields = ['title', 'cover']

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'Enter a title'
                }
            )
        }


class EditListForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = List
        exclude = ['user']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'Title',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Description'
                }
            )
        }


class DeleteListForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = List
        fields = []


class AddMovieToListForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['grade', 'selected_list', 'would_recommend']

    def __init__(self, movie_obj, user, lists, *args, **kwargs):
        super(AddMovieToListForm, self).__init__(*args, **kwargs)
        self.movie_name = movie_obj.name
        self.movie_id = movie_obj.movie_id
        self.user = user
        self.fields['selected_list'].queryset = lists

    def save(self, commit=True):
        movie = super().save(commit=False)
        movie.movie_name = self.movie_name
        movie.movie_id = self.movie_id
        movie.user_id = self.user

        if commit:
            movie.save()

        return movie


class EditMovieFromListForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['grade', 'selected_list', 'would_recommend']

    def __init__(self, lists, *args, **kwargs):
        super(EditMovieFromListForm, self).__init__(*args, **kwargs)
        self.fields['selected_list'].queryset = lists

    def save(self, commit=True):
        self.instance.delete()
        return self.instance


class DeleteMovieFromMovieListForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs['disabled'] = 'disabled'
            field.required = False

    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = Movie
        fields = []
