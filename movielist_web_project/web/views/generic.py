from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView

from movielist_web_project.accounts.models import Profile
from movielist_web_project.web.helpers.mixins import RedirectToDashBoardMixin
from movielist_web_project.web.models import List


class HomeViewNoProfile(RedirectToDashBoardMixin, TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user #FIX NOT NECESSARY
        return context


class Dashboard(LoginRequiredMixin, ListView):
    template_name = 'main/dashboard.html'
    context_object_name = 'lists'

    def get_queryset(self):
        queryset = List.objects.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(pk=self.request.user)
        return context


class AboutView(TemplateView):
    template_name = 'main/about.html'



