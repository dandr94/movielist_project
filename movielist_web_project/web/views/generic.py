from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView

from movielist_web_project.accounts.models import Profile
from movielist_web_project.web.models import List


class HomeViewNoProfile(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')

        return super().dispatch(request, *args, **kwargs)


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



