from django.conf import settings

from django.db import models
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.backends import ModelBackend

from .models import EasyUser

class AuthenticationBackend(ModelBackend):
    @property
    def user_class(self):
        if not hasattr(self, '_user_class'):
            self._user_class = EasyUser
            if not self._user_class:
                raise ImproperlyConfigured('Could not get custom user model')
        return self._user_class

    def get_user(self, user_id):
        try:
            return self.user_class.objects.get(pk=user_id)
        except self.user_class.DoesNotExist:
            return None

    def authenticate(self, **credentials):
        if not self.user_class: return None
        lookup_params = {}
        if getattr(settings, 'ACCOUNT_EMAIL_AUTHENTICATION', False):
            name, identity = "email", credentials.get("email")
        else:
            name, identity = "username", credentials.get("username")
        if identity is None:
            return None
        lookup_params[name] = identity
        try:
            user = self.user_class.objects.get(**lookup_params)
        except self.user_class.DoesNotExist:
            return None
        else:
            if user.check_password(credentials["password"]):
                return user
    
EmailModelBackend = AuthenticationBackend
