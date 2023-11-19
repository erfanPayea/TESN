from django.db import models
from user import models as UserModels

# Create your models here

class Message(models.Model):
    sender = models.ForeignKey(UserModels.User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(UserModels.User, on_delete=models.CASCADE, related_name='received_messages')
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()