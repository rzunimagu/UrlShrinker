from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import CursorPagination
from .models import UrlRedirect
from .serializers import UrlRedirectSerializer
from .utilities import create_new_user
from django.views.generic import TemplateView, RedirectView
from .forms import UrlRedirectForm


class UrlRedirectViewSet(viewsets.ModelViewSet):
    serializer_class = UrlRedirectSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def perform_create(self, serializer):
        if self.request.user.is_anonymous:
            create_new_user(request=self.request)
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_anonymous:
            create_new_user(request=self.request)
        return UrlRedirect.objects.filter(user=self.request.user)


class MainPageView(TemplateView):
    template_name = "shrinker/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Создайте короткую ссылку',
            'form': UrlRedirectForm(),
            'current_site': "{0}://{1}".format(
                self.request.scheme,
                self.request.META['HTTP_HOST'],
            ),
        })
        return context


class RedirectToOriginalUrlView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        url = get_object_or_404(UrlRedirect, url_new=kwargs['url_new'])
        return url.url_original
