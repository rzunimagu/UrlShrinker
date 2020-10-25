from django.views.generic import TemplateView, RedirectView
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from rest_framework import viewsets

from .models import UrlRedirect
from .forms import UrlRedirectForm
from .serializers import UrlRedirectSerializer
from .utilities import create_new_user


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
        if kwargs['url_new'] in cache:
            original_url = cache.get(kwargs['url_new'])
        else:
            original_url = get_object_or_404(UrlRedirect, url_new=kwargs['url_new']).url_original
            cache.set(
                kwargs['url_new'],
                original_url,
                timeout = getattr(settings, 'CACHE_TIMEOUT_SECONDS', DEFAULT_TIMEOUT)
            )
        return original_url
