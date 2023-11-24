from rest_framework.serializers import ModelSerializer
from . import models


class Chat(ModelSerializer):
    class Meta:
        models = models.Chat
        fields = '__all__'


class Message(ModelSerializer):
    class Meta:
        models = models.Chat
        fields = '__all__'
