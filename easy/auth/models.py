from easy.models import easy_model_manager, easy_model
from django.contrib.auth.models import User, UserManager
class EasyUserManager(easy_model_manager, UserManager):
    pass
class User(easy_model, User):
    objects = EasyUserManager()
