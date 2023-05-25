from django.contrib import admin

from account.models import Account
from app.models import PrivatMessage, UnreadMessages


class AuthorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Account)
admin.site.register(PrivatMessage)
admin.site.register(UnreadMessages)