from django.contrib import admin

from ..models import WaitingListEntry



class WaitingListEntryAdmin(admin.ModelAdmin):
    list_display = ["email", "created"]



admin.site.register(WaitingListEntry, WaitingListEntryAdmin)
