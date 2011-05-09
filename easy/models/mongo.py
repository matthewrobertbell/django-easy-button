from easy_models import *
from django_mongodb_engine.contrib import MongoDBManager, MongoDBQuerySet
class easy_mongo_queryset(MongoDBQuerySet, easy_shortcuts_mixin):
    pass
class easy_mongo_manager(MongoDBManager, easy_shortcuts_mixin):
    db = 'mongo'
    def get_query_set(self):
        return easy_mongo_queryset(self.model).using(self.db)
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
