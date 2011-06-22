from easy.random_hashes import *
from django.core import serializers
from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth.models import User

class easy_shortcuts_mixin:
    def a(self):
        return self.all()
    def f(self, *args, **kwargs):
        return self.filter(*args, **kwargs)
    def e(self, *args, **kwargs):
        return self.exclude(*args, **kwargs)
    def g(self, *args, **kwargs):
        try: return self.get(*args, **kwargs)
        except: return None
    def g_c(self, *args, **kwargs):
        return self.get_or_create(*args, **kwargs)
    def g404(self, *args, **kwargs):
        from django.http import Http404
        try: obj = self.g(*args, **kwargs)
        except: raise Http404
        if not obj: raise Http404
        return obj
    def first(self, n=1):
        try: 
            if n == 1: return self.a()[0]
            else: return self.a()[0:n]
        except: return None
    def last(self, n=1):
        qs = self.all()
        if not qs.ordered: qs = qs.order_by('id')
        try: 
            if n == 1: return qs.reverse()[0]
            return qs.reverse()[0:n]
        except: return None
    def to_json(self):
        json_serializer = serializers.get_serializer("json")()
        return json_serializer.serialize(self.a(),
                ensure_ascii=False)

class easy_query_set(QuerySet, easy_shortcuts_mixin):
    pass

class easy_model_manager(models.Manager, easy_shortcuts_mixin):
    use_for_related_fields = True
    def get_query_set(self):
        qs = easy_query_set(self.model, using=self._db)
        qs.a = self.a
        qs.f = self.f
        qs.e = self.e
        qs.g = self.g
        qs.g404 = self.g404
        qs.first = self.first
        qs.last = self.last
        return qs

class easy_model(models.Model):
    objects = easy_model_manager()
    UNIQUE_MAX_TRIES = 15 # Should be enough to get a random until the space fills up
    class UnableToGenerateIDException(Exception):
        pass
    def make_unique(self, prop, generator):
        tries = 0
        while not hasattr(self, prop):
            tries += 1 
            new_val = generator()
            if not self.__class__.g(prop=new_val):
                setattr(self, prop, new_val)
                return new_val
            if tries > self.UNIQUE_MAX_TRIES:
                raise self.UnableToGenerateUniquePropertyException()
    class Meta:
        abstract = True
    @classmethod
    def a(self):
        return self.objects.a()
    @classmethod
    def f(self, *args, **kwargs):
        return self.objects.f(*args, **kwargs)
    @classmethod
    def e(self, *args, **kwargs):
        return self.objects.e(*args, **kwargs)
    @classmethod
    def g(self, *args, **kwargs):
        return self.objects.g(*args, **kwargs)
    @classmethod
    def g404(self, *args, **kwargs):
        return self.objects.g404(*args, **kwargs)
    @classmethod
    def g_c(self, *args, **kwargs):
        return self.objects.g_c(*args, **kwargs)
    @classmethod
    def first(self, *args, **kwargs):
        return self.objects.first(*args, **kwargs)
    @classmethod
    def last(self, *args, **kwargs):
        return self.objects.last(*args, **kwargs)
    def class_name(self):
        return type(self)._meta.object_name
    @classmethod
    def class_name(self):
        return self._meta.object_name


class random_id_model(easy_model):
    id = models.CharField(max_length=128, primary_key=True, blank=True)
    class Meta:
        abstract = True

    def random_id(self):
        return 'RANDOM NOT IMPLEMENTED'
    def save(self, *args, **kwargs):
        self.make_unique('id', self.random_id)
        return super(random_name_model, self).save(*args, **kwargs)

class weak_id_model(random_id_model):
    @classmethod
    def random_id(self):
        return randHash8()
    class Meta:
        abstract = True

class strong_id_model(random_id_model):
    @classmethod
    def random_id(self):
        return randHash40()
    class Meta:
        abstract = True

class silly_named_model(easy_model):
    MAX_LENGTH = 60 # Currently a "soft limit", actual values may exceed this
    class Meta:
        abstract = True

    @classmethod
    def random_name(self):
        from easy.random_names import RANDOM_NAMES
        import random
        return '-'.join(random.sample(RANDOM_NAMES, 4)).lower().replace(' ','-')
    def save(self, *args, **kwargs):
        self.make_unique('id', self.random_id)
        return super(named_model, self).save(*args, **kwargs)


class user_owned_model(strong_id_model):
    user = models.ForeignKey(User)
    class Meta:
        abstract = True
