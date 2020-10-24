import logging
from time import time

from django.db import models
from django.conf import settings

from django.contrib.auth.models import User


logger = logging.getLogger(__name__)


class UrlRedirect(models.Model):
    user = models.ForeignKey(User, verbose_name='Автор', blank=True, on_delete=models.CASCADE, db_index=True)
    url_original = models.URLField(verbose_name='Исходный URL')
    url_new = models.SlugField(verbose_name='Короткий URL', blank=True, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Правило редиректа'
        verbose_name_plural = 'Правила редиректа'
        ordering = ('user', '-pk')

    def __str__(self):
        try:
            host = settings.ALLOWED_HOSTS[0]
        except IndexError:
            host = '127.0.0.1'

        return '{0} -> {1}/{2}'.format(
            self.url_original,
            host,
            self.url_new
        )

    @staticmethod
    def generate_new_url():
        """генерируем новый уникальный URL"""
        url_new = str(hex(int(time())))[2:]
        add_on = 0
        generated_value = url_new
        while UrlRedirect.objects.filter(url_new=generated_value).exists():
            logger.warning("generated url({0}) already exists in database".format(generated_value))
            generated_value = "{0}{1:x}".format(url_new, add_on)
            add_on += 1
        return generated_value
