from django.views.generic import TemplateView, RedirectView
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.shortcuts import render
from django.template import RequestContext

from rest_framework import viewsets

from .models import UrlRedirect
from .forms import UrlRedirectForm
from .serializers import UrlRedirectSerializer
from .utilities import create_new_user

import logging


logger = logging.getLogger(__name__)


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
    """главная страница сайта"""
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
    """перенаправление с коротких ссылок на полные"""

    def get_redirect_url_cache(self, *args, **kwargs):
        """выдаем редирект с использованием кеша"""
        if kwargs['url_new'] in cache:
            original_url = cache.get(kwargs['url_new'])
        else:
            original_url = get_object_or_404(UrlRedirect, url_new=kwargs['url_new']).url_original
            cache.set(
                kwargs['url_new'],
                original_url,
                timeout=getattr(settings, 'CACHE_TIMEOUT_SECONDS', DEFAULT_TIMEOUT)
            )
        return original_url

    def get_redirect_url_nocache(self, *args, **kwargs):
        """выдаем редирект без использования кеша"""
        original_url = get_object_or_404(UrlRedirect, url_new=kwargs['url_new']).url_original
        return original_url

    def get_redirect_url(self, *args, **kwargs):
        return self.get_redirect_url(*args, **kwargs)


def handler404(request, *args, **kwargs):
    response = render(
        request,
        template_name='shrinker/404.html',
        context={
            'title': 'Страница не найдена'
        },
        status=404
    )
    logger.error("404. path: {0}. args:{1}. kwargs{2} ".format(request.path, args, kwargs))
    return response


def handler500(request, *args, **kwargs):
    response = render(
        request,
        template_name='shrinker/error.html',
        context={
            'title': 'Ошибка',
            'email': getattr(settings, 'ADMIN_EMAIL', 'email@domain.com')
        },
        status=500
    )
    logger.error("Error. path: {0}. args:{1}. kwargs{2} ".format(request.path, args, kwargs))
    return response
