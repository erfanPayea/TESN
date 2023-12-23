from django.db import models
from project.user import models as user_models

# Create your models here


class Chat(models.Model):
    first_user = models.ForeignKey(user_models.User, on_delete=models.SET_NULL, related_name='chat_starter', null=True)
    second_user = models.ForeignKey(user_models.User, on_delete=models.SET_NULL, related_name='chat_member', null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(user_models.User, on_delete=models.SET_NULL, related_name='sent_messages', null=True)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

