from django.conf.urls.defaults import *


urlpatterns = patterns("",
    url(r'^account/', include('easy.account.urls')),
)
