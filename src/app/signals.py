from django.db.models.signals import post_save
from django.dispatch import receiver

from app.models import PrivatMessage


@receiver(post_save, sender=PrivatMessage)
def unreaded_messages_reload(sender,instance,**kwargs):
    print("aaaaaaaaaaa")
