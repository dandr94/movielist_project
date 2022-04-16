from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView
from movielist_web_project.accounts.forms import CreateProfileForm, EditProfileForm, ChangePasswordForm
from movielist_web_project.accounts.models import Profile
from movielist_web_project.web.forms import LoginUserForm
from movielist_web_project.web.helpers.helper_functions import return_list_with_additional_stats
from movielist_web_project.web.helpers.mixins import RedirectToDashBoardMixin, HideHeaderAndFooterMixin

from movielist_web_project.web.models import Movie, List


class RegisterUserView(HideHeaderAndFooterMixin, CreateView):
    form_class = CreateProfileForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, *args, **kwargs):
        result = super().form_valid(*args, **kwargs)
        login(self.request, self.object)
        return result


class LoginUserView(RedirectToDashBoardMixin, HideHeaderAndFooterMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'accounts/signin.html'

    def get_success_url(self):
        return reverse_lazy('dashboard')


class LogoutUserView(LogoutView):
    pass


class ProfileDetailsView(DeleteView):
    model = Profile
    template_name = 'accounts/profile_details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_lists'] = List.objects.filter(user_id=self.object.user_id)
        context['all_lists_count'] = len(context['all_lists'])
        context['all_movies'] = Movie.objects.filter(user_id=self.object.user_id)
        context['all_movies_count'] = len(context['all_movies'])
        if context['all_movies_count']:
            context['average_grade'] = \
                f"{sum([x.grade for x in context['all_movies']]) / context['all_movies_count']:.2f}"
        else:
            context['average_grade'] = 0
        context['lists'] = return_list_with_additional_stats(context['all_lists'], context['all_movies'])
        context['is_owner'] = self.object.user_id == self.request.user.id
        return context


@login_required
def profile_edit(request, pk):
    profile = Profile.objects.get(pk=pk)
    is_owner = request.user.id == profile.user_id

    if not is_owner:
        raise PermissionDenied

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile details', pk)
    else:
        form = EditProfileForm(instance=profile)

    context = {
        'form': form,
        'profile': profile,
        'hide_header': True,
        'hide_footer': True,
    }

    return render(request, 'accounts/profile_edit.html', context)


class ChangeUserPasswordView(LoginRequiredMixin, HideHeaderAndFooterMixin, PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'accounts/profile_change_password.html'
    success_url = reverse_lazy('dashboard')

