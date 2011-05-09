from contrib.random_hashes import *
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


class weak_id_model(easy_model):
    id = models.CharField(max_length=40, primary_key=True,
            default=randHash8, blank=True)
    class Meta:
        abstract = True

class strong_id_model(easy_model):
    id = models.CharField(max_length=40, primary_key=True,
            default=randHash40, blank=True)
    class Meta:
        abstract = True

class user_owned_model(weak_id_model):
    user = models.ForeignKey(User)
    class Meta:
        abstract = True

try:
    from django_mongodb_engine.contrib import MongoDBManager, MongoDBQuerySet
    class easy_mongo_queryset(MongoDBQuerySet, easy_shortcuts_mixin):
        pass
    class easy_mongo_manager(MongoDBManager, easy_shortcuts_mixin):
        db = 'mongo'
        def get_query_set(self):
            return easy_mongo_queryset(self.model).using('mongo')
    class easy_mongo_model(easy_model):
        objects = easy_mongo_manager()
        unique = models.CharField(max_length=1024, 
                unique=True, db_index=True)
        unique_len = 8
        db = 'mongo'
        @classmethod
        def find(klass, uid):
            return klass.objects.g(unique=uid)
        @classmethod
        def f404(klass, uid):
            return klass.objects.g404(unique=uid)
        def save(self, *args, **kwargs):
            if not self.unique or len(self.unique) == 0:
                self.unique = randHash40()[:self.unique_len]
            return super(easy_mongo_model, self).save(*args,**kwargs)
        class Meta:
            abstract = True
except:
    pass # No mongodb support
