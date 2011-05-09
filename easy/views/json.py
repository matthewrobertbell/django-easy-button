from django.db import models
from django.core.serializers import base
from django.db import models
from django.core.serializers.json import DateTimeAwareJSONEncoder
import sys
from traceback import print_exc
from django.utils.simplejson.decoder import JSONDecoder
from django.http import HttpResponse

def jsonmethod(f):
   """
      A simple proxy used to indicate that the given method is in fact
      available to json clients.
   """
   f.json_public = True
   return f

class MySerializer(base.Serializer):
    """
    Serializes a QuerySet to basic Python objects.
    """
    
    def start_serialization(self):
        self._current = None
        self.objects = []
        
    def end_serialization(self):
        pass
        
    def start_object(self, obj):
        self._current = {
            "model"  : str(obj._meta),
            "pk"     : str(obj._get_pk_val()),
        }
        
    def end_object(self, obj):
        self.objects.append(self._current)
        self._current = None
        
    def handle_field(self, obj, field):
        if isinstance(field, models.FileField) or isinstance(field, models.DateTimeField):
           self._current[field.name] = self.get_string_value(obj, field)
        else:
           self._current[field.name] = getattr(obj, field.name)
        
    def handle_fk_field(self, obj, field):
        related = getattr(obj, field.name)
        if related is not None:
            related = related._get_pk_val()
        self._current[field.name] = related
    
    def handle_m2m_field(self, obj, field):
        self._current[field.name] = [related._get_pk_val() for related in getattr(obj, field.name).iterator()]
    
    def getvalue(self):
        return self.objects[0]

class DjangoAwareJSONEncoder(DateTimeAwareJSONEncoder):
   def default(self, o):
      if isinstance(o, models.Model):
         return MySerializer().serialize([o])
      else:
         return super(DjangoAwareJSONEncoder, self).default(o)

         
class JSONService(object):   
   """
      Wrapper for a view func to indicate that it should de-serialize any
      POST json inputs and serialize the return value into a json result.
      
      Be sure to define a getMethodImplementation() or a put @jsonmethod
      in front of each public method.
   """

   class Error(Exception):
      """
         Raise this exception type to return an error to the client from
         an rpc handling method
      """
      def __init__(self, code=0, message='error'):
         self.code = code
         self.message = message
         
      def asDict(self):
         return {"code":self.code, "message":self.message}
   
   def getMethodImplementation(self, name):
      """
         Get the implementation of a method by method name._
      """
      
      try:
         f = getattr(self, name)
      except AttributeError:
         return None
      try:
         if f.im_func.json_public:
            return f
      except AttributeError:
         pass
      try:
         if f.json_public:
            return f
      except AttributeError:
         pass
      return None
   
   def getAvailableMethods(self):
      return self.__class__.__json_rpc_methods__
   
   def makeResponse(self, id, result, code=0, error=None):
      if error or code: error = {"code":code, "message":error}
      return {"result":result, "id":id, "error":error}
   
   def __call__(self, request, *args, **kwargs):
      
      if len(request.POST):
         rpcRequest = JSONDecoder().decode(request.raw_post_data)
      else:
         rpcRequest = dict(request.GET)
         try: rpcRequest['params'] = JSONDecoder().decode(request['params'])
         except KeyError: pass
         
         
      #print 'attempting call ... ', rpcRequest
      
      id = None
      params = None
      errorCode = 0
      try:
         method = rpcRequest["method"]
      except KeyError:  
         result = None       
         error = "Invalid JSON-RPC request; method must be specified: %r"%(rpcRequest) # Not a JSON request
      else:
         try: params = rpcRequest["params"]
         except KeyError: params = None
         try: id = rpcRequest["id"]
         except KeyError: id = None
         try: mode = request["mode"]
         except KeyError: mode = "json"
         try:
            f = self.getMethodImplementation(method)
            if f:
               if params is not None: args = list(args).extend(params)
               try: func = f.im_func
               except AttributeError: func = f
               argnames = func.func_code.co_varnames[len(params):func.func_code.co_argcount]
               for var in ("request", "rpcRequest", "id", "method"):
                  if var in argnames:
                     kwargs[var] = locals()[var]
               result = f(*params, **kwargs)
               error = None
            else:
               result = None
               error = "No such method %r; available methods are %r"%(method, self.getAvailableMethods())

         except JSONService.Error, x:
            errorCode = x.code
            error = x.message
            result = None
         except:
         #   stackTrace = StringIO()
            print 'exception raised'
            sys.stdout.flush()
            print_exc()
            sys.stderr.flush()
            raise
    
      #   error = stackTrace.getvalue()
      #   result = None
      
      response = self.makeResponse(id, result, errorCode, error)
      #print 'response', response
      json = DjangoAwareJSONEncoder(ensure_ascii=False).iterencode(response)
      if mode == "json":
         return HttpResponse(json, mimetype='application/json')
      elif mode == "text":
         return HttpResponse(json, mimetype='text/plain')
