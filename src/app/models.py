from asgiref.sync import sync_to_async
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


class PrivatMessage(models.Model):
    messages = models.FileField(upload_to="static/messages")
    first_account = models.ForeignKey("account.Account",related_name="first_account",on_delete=models.CASCADE)
    second_account = models.ForeignKey("account.Account",related_name="second_account",on_delete=models.CASCADE)

    connected_to_chat = models.CharField(default="", max_length=120)


    who_start_stream = models.CharField(max_length=50, null=True)

    #def __str__(self):
     #   return f"Chat({self.first_account.username} | {self.second_account.username})"
@receiver(post_save, sender=PrivatMessage)
def mymodel_presave(sender, instance, **kwargs):
    print("Instance------------>",instance)


class UnreadMessages(models.Model):
    account = models.ForeignKey("account.Account",related_name="user_unread", on_delete=models.CASCADE)
    receiver_accounts = models.ForeignKey("account.Account",related_name="receiver_unread", on_delete=models.CASCADE)
    room = models.ForeignKey("app.PrivatMessage", related_name="unread_room", on_delete=models.CASCADE)
    count_unread = models.IntegerField(default=0)
