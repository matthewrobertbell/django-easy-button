from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from easy.models import easy_model



class WaitingListEntry(easy_model):
    email = models.EmailField(_("email address"), unique=True)
    created = models.DateTimeField(_("created"), default=datetime.now, editable=False)
    
    class Meta:
        verbose_name = _("waiting list entry")
        verbose_name_plural = _("waiting list entries")
