from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView, ListView, DeleteView, CreateView

from movielist_web_project.web.forms import DeleteMovieFromMovieListForm, CreateListForm, \
    EditListForm, DeleteListForm
from movielist_web_project.web.helpers.mixins import PermissionHandlerMixin, HideHeaderAndFooterMixin
from movielist_web_project.web.models import Movie, List

UserModel = get_user_model()


class CreateMovieListView(LoginRequiredMixin, CreateView):
    form_class = CreateListForm
    template_name = 'main/list_create.html'
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class EditMovieListView(LoginRequiredMixin, HideHeaderAndFooterMixin, PermissionHandlerMixin, UpdateView):
    model = List
    template_name = 'main/list_edit.html'
    form_class = EditListForm
    success_url = reverse_lazy('dashboard')


class DeleteMovieListView(LoginRequiredMixin, HideHeaderAndFooterMixin, PermissionHandlerMixin, DeleteView):
    template_name = 'main/list_delete.html'
    form_class = DeleteListForm
    model = List
    success_url = reverse_lazy('dashboard')


class DetailsMovieListView(ListView):
    model = Movie
    template_name = 'main/list_details.html'
    context_object_name = 'movie_list'

    def get_queryset(self):
        queryset = Movie.objects.filter(selected_list_id=self.kwargs["pk"]).order_by('-grade')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = List.objects.get(id=self.kwargs['pk'])
        context['lists'] = List.objects.filter(user_id=self.request.user.id)
        context['hide_footer'] = True
        context['is_owner'] = self.request.user.id == context['list'].user_id
        return context


class DeleteMovieFromMovieList(LoginRequiredMixin, HideHeaderAndFooterMixin, PermissionHandlerMixin, DeleteView):
    model = Movie
    template_name = 'main/list_movie_delete.html'
    form_class = DeleteMovieFromMovieListForm
    success_url = reverse_lazy('dashboard')
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.request.user.id == self.object.user_id

        return context
