from django.db import models
from user import models as UserModels

# Create your models here

class Chat(models.Model):
    sender = models.ForeignKey(UserModels.User, on_delete=models.CASCADE, related_name='chat_starter')
    receiver = models.ForeignKey(UserModels.User, on_delete=models.CASCADE, related_name='chat_member')
    created_at = models.DateTimeField(auto_now_add=True)
class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

