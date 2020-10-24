import logging
from rest_framework import serializers
from rest_framework import validators
from .models import UrlRedirect
from django.contrib.auth.models import User


logger = logging.getLogger(__name__)


class UrlRedirectSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlRedirect
        fields = ['pk', 'url_original', 'url_new']

    def validate_url_new(self, value):
        if value in ['admin', 'api', '404']:
            raise serializers.ValidationError("Указанный короткий УРЛ уже занят")
        else:
            return value or UrlRedirect.generate_new_url()

    def save(self, **kwargs):
        self.validated_data['user'] = kwargs.get('user')
        logger.debug("{0} create redirect {1} -> {2}".format(
            self.validated_data['user'],
            self.validated_data['url_original'],
            self.validated_data['url_new'],
        ))
        return super().save()


class UserNameSerializer(serializers.Serializer):
    username = serializers.SlugField(validators=[validators.UniqueValidator(queryset=User.objects.all())])
