from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django import forms

from movielist_web_project.accounts.models import Profile
from movielist_web_project.web.helpers.mixins import CssStyleFormMixin

UserModel = get_user_model()


class CreateProfileForm(CssStyleFormMixin, UserCreationForm):
    username = forms.CharField(
        max_length=Profile.USERNAME_MAX_CHAR
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_css_style_form_controls()
        for field_name in ['username', 'email', 'password1', 'password2']:
            self.fields[field_name].help_text = None

    def save(self, commit=True):
        user = super().save(commit=commit)

        profile = Profile(
            username=self.cleaned_data['username'],
            user=user
        )

        if commit:
            profile.save()
        return user

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password1', 'password2']


class EditProfileForm(CssStyleFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_css_style_form_controls()

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'facebook', 'instagram', 'twitter', 'website']


class ChangePasswordForm(CssStyleFormMixin, PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_css_style_form_controls()

    class Meta:
        model = Profile
        fields = ['old_password', 'new_password1', 'new_password2']