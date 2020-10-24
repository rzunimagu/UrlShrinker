import logging
from uuid import uuid4
from django.contrib.auth.models import User
from django.contrib.auth import login

from shrinker.serializers import UserNameSerializer

logger = logging.getLogger(__name__)


def create_new_user(request):
    """создаем нового пользователя"""
    user_name = UserNameSerializer(data={'username': request.session.get('username', None)})
    while not user_name.is_valid():
        request.session['username'] = str(uuid4())
        user_name = UserNameSerializer(data={'username': request.session.get('username')})
    created_user = User(username=user_name.data['username'])
    created_user.set_unusable_password()
    created_user.save()
    logger.debug("create new user {0}".format(user_name.data['username']))
    login(request, created_user)
