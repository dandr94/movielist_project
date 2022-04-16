from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


class RedirectToDashBoardMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')

        return super().dispatch(request, *args, **kwargs)


class HideHeaderAndFooterMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hide_header'] = True
        context['hide_footer'] = True
        return context


class CssStyleFormMixin:
    fields = {}

    def _init_css_style_form_controls(self):
        for _, field in self.fields.items():
            if not hasattr(field.widget, 'attrs'):
                setattr(field.widget, 'attrs', {})
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = ''
            field.widget.attrs['class'] += 'sign__input'


class PermissionHandlerMixin:
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        owner = self.request.user.id == self.object.user_id
        if not owner and not request.user.is_superuser:
            raise PermissionDenied
        return response