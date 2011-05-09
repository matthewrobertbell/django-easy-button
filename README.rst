**django's easy button**

Writing django is great, but coming from Rails roots, a few things have always
felt missing.

- Extended models with ``easy.models.easy_model``, which has several derivatives, such as ``strong_id_model`` (primary key is a random varchar(40)), ``weak_id_model`` (same, but with varchar(8)), and ``user_owned_model`` (a ``weak_id_model`` with a foreign key to the users table)
  ::
    class Address(easy.models.user_owned_model):
      country = models.CharField(max_length=128)

    a= Address.objects.create(user_id=1, country="US")
    a.save()
    a.id #=> 'a8zf139d'
    a.user #=> <User: linked>
- Quick and easy model lookup shorthand
  ::
    # Shortcut methods work with-or-without ".object"
    # .first(), .last(), .random() are obvious --
    Address.first()

    # Shortcuts for common lookups
    # a = all, f = filter, e = exclude, g = get_or_none, g404 = get_or_404
    user_address = Address.g(pk='', user=req.user) or Address(user=req.user)

    # Chaining still works
    Address.f(user=req.user).e(country='US').first()
    
- "Scoping" -- really just dynamic lookup aliasing (still in development).
  ::
    class LogMessage(easy.models.strong_id_model):
      level = models.CharField(max_length=128)
      def __init__(self,*args,**kwargs):
        super(LogMessage,self).__init__(*args,**kwargs)
        self.scope('errors', lambda qs: qs.f(level='error'))

    # Now you can do, e.g. ->
    LogMessage.errors().count() 
        
- ``easy.views`` -- making rapidly developing front-ends suck less
  by drastically cutting the required code for common tasks
  :: 
    # Lists of objects owned by a user
    # ("Event" must be a user_owned_model, or relation must be specified)
    def my_events(req):
        return user_object_list(req, Event.a(), 
            relation='user_id',
            template='events/object_list.html'})

    # Or get a single object for the user
    # Throws a 404 if not found
    def event_info(req, id):
        a = 5
        return user_object_detail(req, Event.f(pk=id),
                relation='user_id',
                template='events/info.html',
                extra_context={'a_value': a})

    # A "new-or-edit" form
    # Called with an id, this form is for editing
    # Called without an id, the form is for creating
    def event_form(req, id=False):
        return user_form_page(req, Event, EventForm, 
                instance=Event.find(id),
                redirect_to='/events/{id}')
- mongodb support: ``easy.models.mongo`` has basic support for adding the
  ``easy_queries_mixin`` to mongodb-engine models, if you're using it.

**that was easy**
